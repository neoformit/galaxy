<template>
    <upload-wrapper
        ref="wrapper"
        :top-info="topInfo"
        :highlight-box="highlightBox"
    >
        <div v-show="showHelper" class="upload-helper"><i class="fa fa-files-o" />Extract an archive to your history</div>
        <div v-show="!showHelper" ref="archiveTree">
            <ArchiveTree :elements="archiveElements" />
        </div>
        <template v-slot:footer>
            <span class="upload-footer-title">Archive type:</span>
            <select2
                ref="footerExtension"
                v-model="extension"
                container-class="upload-footer-extension"
                :enabled="!running">
                <option v-for="(ext, index) in extensions" :key="index" :value="ext.id">{{ ext.text }}</option>
            </select2>
            <span class="upload-footer-extension-info upload-icon-button fa fa-search" />

            <span class="upload-footer-title">Extract to:</span>
            <select
                ref="footerExtractTo"
                v-model="extractTo"
                container-class="upload-footer-extension"
                :enabled="!running">
                <option value="datasets">Datasets</option>
                <option value="collection">Collection</option>
            </select>

            <span class="upload-footer-title">Specification:</span>
            <select
                ref="footerSpecification"
                v-model="extractFrom"
                container-class="upload-footer-extension"
                :enabled="!running">
                <option value="archive">None</option>
                <option value="bagit_archive">BagIt</option>
                <option value="rocrate_archive">RO-crate</option>
            </select>
        </template>
        <template v-slot:buttons>
            <!-- TODO: these would be used to start the upload after archive contents have been selected -->
            <b-button
                id="btn-close"
                ref="btnClose"
                class="ui-button-default upload-close"
                :title="btnCloseTitle"
                @click="$emit('dismiss')">
                {{ btnCloseTitle }}
            </b-button>
            <b-button
                id="btn-reset"
                ref="btnReset"
                class="ui-button-default"
                :title="btnResetTitle"
                :disabled="!enableReset"
                @click="_eventReset">
                {{ btnResetTitle }}
            </b-button>
            <b-button
                id="btn-stop"
                ref="btnStop"
                class="ui-button-default"
                :title="btnStopTitle"
                :disabled="counterRunning == 0"
                @click="_eventStop">
                {{ btnStopTitle }}
            </b-button>
            <b-button
                id="btn-start"
                ref="btnStart"
                class="ui-button-default upload-start"
                :disabled="!enableStart"
                :title="btnStartTitle"
                :variant="enableStart ? 'primary' : ''"
                @click="_eventStart">
                {{ btnStartTitle }}
            </b-button>
            <b-button
                id="btn-new"
                ref="btnCreate"
                class="ui-button-default upload-paste"
                :title="btnCreateTitle"
                :disabled="!enableSources"
                @click="_eventCreate()">
                <span class="fa fa-edit"></span>{{ btnCreateTitle }}
            </b-button>
            <b-button
                v-if="remoteFiles"
                id="btn-ftp"
                ref="btnFtp"
                class="ui-button-default"
                :disabled="!enableSources"
                @click="_eventRemoteFiles">
                <span class="fa fa-folder-open-o"></span>{{ btnFilesTitle }}
            </b-button>
            <b-button
                id="btn-local"
                ref="btnLocal"
                class="ui-button-default"
                :title="btnLocalTitle"
                :disabled="!enableSources"
                @click="uploadSelect">
                <span class="fa fa-laptop"></span>{{ btnLocalTitle }}
            </b-button>
        </template>
    </upload-wrapper>
</template>

<script>
import { BButton } from "bootstrap-vue";
import { uploadModelsToPayload } from "./helpers";
import ArchiveTree from "./ArchiveTree";

// TODO: Handle/pass extensions tar, zip, bagit, yaml etc?
// These are hard-coded for now

export default {
    components: { BButton },
    props: {

    },
    data() {
        return {
            uploadUrl: '/api/',
            topInfo: "",
            highlightBox: false,
            showHelper: true,
            extractTo: 'datasets',
            extractFrom: 'archive',
            extension: this.details.defaultExtension,
            listExtensions: [],
            running: false,
            enableReset: false,
            enableStart: false,
            enableSources: false,
            btnLocalTitle: _l("Choose local files"),
            btnCreateTitle: _l("Paste/Fetch data"),
            btnStartTitle: _l("Start"),
            btnStopTitle: _l("Pause"),
            btnResetTitle: _l("Reset"),
            archiveElements: [],
        };
    },
    computed: {
        extensions() {
            // TODO: How do we handle archive extensions? Where do they come from?
            const archive_extensions = [
                'tar',
                'zip',
                // 'yaml',    // yaml description?
            ];
            return this.listExtensions.filter((ext) => archive_extensions.includes(ext.id));
        },
        appModel() {
            return this.details.model;  // TODO: what does 'details' contain?
        },
    },
    created() {

    },
    mounted() {

    },
    methods: {
        _eventStart() {
            // Build collection of files for upload before start (UploadBoxMixin)

            // Be good if we could just create a set of standard upload rows with selected elements?
            // Rows should point to temp files for upload but need to defer extraction until upload..?

            // Then call uploadModelsToPayload()
        },
        _eventStop() {

        },
        _eventReset() {

        },
    },
}
</script>
<style lang="">
    
</style>