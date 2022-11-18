<template>
    <div class="container">
        <div class="row justify-content-md-center">
            <template v-if="!confirmURL">
                <div class="col col-lg-6">
                    <b-alert :show="!!messageText" :variant="messageVariant">
                        {{ messageText }}
                    </b-alert>
                    <b-alert :show="!!connectExternalURL" variant="info">
                        Reminder: Registration and usage of multiple accounts is tracked and such accounts are subject
                        to termination and data deletion. Connect existing account now to avoid possible loss of data.
                    </b-alert>
                    <b-form id="login" @submit.prevent="submitLogin()">
                        <b-card no-body>
                            <b-card-header>
                                <span v-if="!connectExternalURL"> Welcome to Galaxy, please log in </span>
                                <span v-else>
                                    There already exists a user with the email <i>{{ connectExternalURL }}</i
                                    >. To associate this external login, you must first be logged in as that existing
                                    account.
                                </span>
                            </b-card-header>
                            <b-card-body>
                                <div>
                                    <!-- standard internal galaxy login -->
                                    <b-form-group label="Public Name or Email Address">
                                        <b-form-input
                                            v-if="!connectExternalURL"
                                            v-model="login"
                                            name="login"
                                            type="text" />
                                        <b-form-input
                                            v-else
                                            disabled
                                            :value="connectExternalURL"
                                            name="login"
                                            type="text" />
                                    </b-form-group>
                                    <b-form-group label="Password">
                                        <b-form-input v-model="password" name="password" type="password" />
                                        <b-form-text>
                                            Forgot password?
                                            <a href="javascript:void(0)" role="button" @click="reset"
                                                >Click here to reset your password.</a
                                            >
                                        </b-form-text>
                                    </b-form-group>
                                    <b-button name="login" type="submit">Login</b-button>
                                </div>
                                <div v-if="enable_oidc">
                                    <!-- OIDC login-->
                                    <external-login :login_page="true" />
                                </div>
                            </b-card-body>
                            <b-card-footer>
                                <span v-if="!connectExternalURL">
                                    Don't have an account?
                                    <span v-if="allowUserCreation">
                                        <a
                                            id="register-toggle"
                                            href="javascript:void(0)"
                                            role="button"
                                            @click.prevent="toggleLogin">
                                            Register here.
                                        </a>
                                    </span>
                                    <span v-else>
                                        Registration for this Galaxy instance is disabled. Please contact an
                                        administrator for assistance.
                                    </span>
                                </span>
                                <span v-else>
                                    Do not wish to connect to an external provider?
                                    <a href="javascript:void(0)" role="button" @click.prevent="returnToLogin"
                                        >Return to login here.</a
                                    >
                                </span>
                            </b-card-footer>
                        </b-card>
                    </b-form>
                </div>
            </template>

            <template v-else>
                <new-user-confirmation @setRedirect="setRedirect" />
            </template>

            <div v-if="show_welcome_with_login" class="col">
                <b-embed type="iframe" :src="welcome_url" aspect="1by1" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import { getGalaxyInstance } from "app";
import { getAppRoot } from "onload";
import NewUserConfirmation from "components/login/NewUserConfirmation.vue";
import ExternalLogin from "components/User/ExternalIdentities/ExternalLogin.vue";

Vue.use(BootstrapVue);

export default {
    components: {
        ExternalLogin,
        NewUserConfirmation,
    },
    props: {
        show_welcome_with_login: {
            type: Boolean,
            required: false,
        },
        welcome_url: {
            type: String,
            required: false,
        },
    },
    data() {
        const galaxy = getGalaxyInstance();
        return {
            login: null,
            password: null,
            url: null,
            messageText: null,
            messageVariant: null,
            allowUserCreation: galaxy.config.allow_user_creation,
            redirect: galaxy.params.redirect,
            session_csrf_token: galaxy.session_csrf_token,
            enable_oidc: galaxy.config.enable_oidc,
        };
    },
    computed: {
        messageShow() {
            return this.messageText != null;
        },
        confirmURL() {
            var urlParams = new URLSearchParams(window.location.search);
            return urlParams.has("confirm") && urlParams.get("confirm") == "true";
        },
        connectExternalURL() {
            var urlParams = new URLSearchParams(window.location.search);
            return urlParams.get("connect_external");
        },
        welcomeUrlWithRoot() {
            return safePath(this.welcomeUrl);
        },
    },
    methods: {
        toggleLogin() {
            if (this.$root.toggleLogin) {
                this.$root.toggleLogin();
            }
        },
        submitLogin() {
            let redirect = this.redirect;
            if (this.connectExternalURL) {
                this.login = this.connectExternalURL;
            }
            if (localStorage.getItem("redirect_url")) {
                this.redirect = localStorage.getItem("redirect_url");
            }
            const rootUrl = getAppRoot();
            axios
                .post(`${rootUrl}user/login`, this.$data)
                .then((response) => {
                    if (response.data.message && response.data.status) {
                        alert(response.data.message);
                    }
                    if (data.expired_user) {
                        window.location = safePath(`/root/login?expired_user=${data.expired_user}`);
                    } else if (data.redirect) {
                        window.location = encodeURI(data.redirect);
                    } else if (this.connectExternalURL) {
                        window.location = safePath("/user/external_ids?connect_external=true");
                    } else {
                        window.location = `${rootUrl}`;
                    }
                })
                .catch((error) => {
                    this.messageVariant = "danger";
                    const message = error.response.data && error.response.data.err_msg;
                    if (this.connectExternalURL && message && message.toLowerCase().includes("invalid")) {
                        this.messageText =
                            message + " Try logging in to the existing account through an external provider below.";
                    } else {
                        this.messageText = message || "Login failed for an unknown reason.";
                    }
                });
        },
        setRedirect(url) {
            localStorage.setItem("redirect_url", url);
        },
        reset(ev) {
            const rootUrl = getAppRoot();
            ev.preventDefault();
            axios
                .post(`${rootUrl}user/reset_password`, { email: this.login })
                .then((response) => {
                    this.messageVariant = "info";
                    this.messageText = response.data.message;
                })
                .catch((error) => {
                    this.messageVariant = "danger";
                    const message = error.response.data && error.response.data.err_msg;
                    this.messageText = message || "Password reset failed for an unknown reason.";
                });
        },
        returnToLogin() {
            window.location = safePath("/login/start");
        },
    },
};
</script>
<style scoped>
.card-body {
    overflow: visible;
}
</style>
