<template>
    <upload-wrapper
        ref="wrapper"
        :top-info="topInfo"
        :highlight-box="highlightBox"
    >
        <div v-show="showHelper" class="upload-helper"><i class="fa fa-files-o" />Upload an archive in Tar, Zip or Bagit format</div>
        <table v-show="!showHelper" ref="uploadTable" class="upload-table ui-table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Size</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th />
                </tr>
            </thead>
            <tbody />
        </table>
        <template v-slot:footer>
            <span class="upload-footer-title">Type (set all):</span>
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
        </template>
        <template v-slot:buttons>
            <!-- TODO: Not sure if these all make sense in "archive wizard" flow -->
            <!-- Do we allow multiple archives to be selected or is it a single-archive operation? -->
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
import UploadRow from "mvc/upload/default/default-row";
import UploadBoxMixin from "./UploadBoxMixin";
import { BButton } from "bootstrap-vue";

// TODO: Handle/pass extensions tar, zip, bagit, yaml (others?)
// Can we just hard-code these?

/*
- What does this.details [Obj] contain?
    # UploadModalContent:157
    details() {
        return {
            effectiveExtensions: this.effectiveExtensions,
            listGenomes: this.listGenomes,
            currentFtp: this.currentFtp,
            fileSourcesConfigured: this.fileSourcesConfigured,
            defaultExtension: this.defaultExtension,
            defaultDbKey: this.defaultDbKey,
            uploadPath: this.uploadPath,
            model: this.model,
            chunkUploadSize: this.chunkUploadSize,
            history_id: this.currentHistoryId,
        };
    },

- this.initCollection()
    # UploadBoxMixin:329
    this.collection = new UploadModel.Collection();

- this.initAppProperties()
    # UploadBoxMixin:329
    this.listExtensions = this.details.effectiveExtensions;
    this.listGenomes = this.details.listGenomes;
    this.ftpUploadSite = this.details.currentFtp;
    this.fileSourcesConfigured = this.details.fileSourcesConfigured;

- this.collection - is it a galaxy collection or something else?
    See this.initCollection() above
*/

export default {
    components: { BButton },
    mixins: [UploadBoxMixin],
    props: {
        multiple: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            uploadUrl: '/api/',
            // Doesn't make too much sense to upload multiple if we're going to have an extract wizard...
            multiple: false,
            topInfo: "",
            highlightBox: false,
            showHelper: true,
            extractTo: 'datasets',
            extension: this.details.defaultExtension,
            listExtensions: [],
            running: false,
            rowUploadModel: UploadRow,
            counterAnnounce: 0,
            counterSuccess: 0,
            counterError: 0,
            counterRunning: 0,
            uploadSize: 0,
            uploadCompleted: 0,
            enableReset: false,
            enableStart: false,
            enableSources: false,
            btnLocalTitle: _l("Choose local files"),
            btnCreateTitle: _l("Paste/Fetch data"),
            btnStartTitle: _l("Start"),
            btnStopTitle: _l("Pause"),
            btnResetTitle: _l("Reset"),
        };
    },
    computed: {
        extensions() {
            // TODO: How do we handle archive extensions? Where do they come from?
            const archive_extensions = [
                'tar',
                'zip',
                'bagit',
                'yaml', // yaml description?
            ];
            return this.listExtensions.filter((ext) => archive_extensions.includes(ext.id));
        },
        appModel() {
            return this.details.model;  // TODO: what does 'details' contain?
        },
    },
    watch: {
        extension: function (value) {
            this.updateExtension(value);
        },
    },
    created() {
        this.initCollection();     // TODO: where does this come from?
        this.initAppProperties();  // TODO: where does this come from?
    },
    mounted() {
        this.initExtensionInfo();
        this.initFtpPopover();
        // file upload
        this.initUploadbox({
            initUrl: (index) => {
                if (!this.uploadUrl) {
                    this.uploadUrl = this.getRequestUrl([this.collection.get(index)], this.history_id);
                }
                return this.uploadUrl;
            },
            multiple: this.multiple,
            announce: (index, file) => {
                this._eventAnnounce(index, file);
            },
            initialize: (index) => {
                return uploadModelsToPayload([this.collection.get(index)], this.history_id);
            },
            progress: (index, percentage) => {
                this._eventProgress(index, percentage);
            },
            success: (index, message) => {
                this._eventSuccess(index, message);
            },
            error: (index, message) => {
                this._eventError(index, message);
            },
            warning: (index, message) => {
                this._eventWarning(index, message);
            },
            complete: () => {
                this._eventComplete();
            },
            ondragover: () => {
                this.highlightBox = true;
            },
            ondragleave: () => {
                this.highlightBox = false;
            },
            chunkSize: this.details.chunkUploadSize,
        });
        this.collection.on("remove", (model) => {
            this._eventRemove(model);
        });
        this._updateStateForCounters();
    },
    methods: {
        _newUploadModelProps: function (index, file) {
            return {
                id: index,
                file_name: file.name,
                file_size: file.size,
                file_mode: file.mode || "local",
                file_path: file.path,
                file_uri: file.uri,
                file_data: file,
            };
        },

        /** Success */
        _eventSuccess: function (index) {
            const it = this.collection.get(index);
            it.set({ percentage: 100, status: "success" });
            this._updateStateForSuccess(it);
        },

        /** Remove all */
        _eventReset: function () {
            if (this.counterRunning === 0) {
                this.collection.reset();
                this.counterAnnounce = 0;
                this.counterSuccess = 0;
                this.counterError = 0;
                this.counterRunning = 0;
                this.uploadbox.reset();
                this.extension = this.details.defaultExtension;
                this.genome = this.details.defaultDbKey;
                this.appModel.set("percentage", 0);
                this._updateStateForCounters();
            }
        },
    },
}
</script>
<style lang="">
    
</style>