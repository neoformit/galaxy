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
                id="btn-history"
                ref="btnHistory"
                class="ui-button-default"
                :title="btnHistoryTitle"
                :disabled="!enableSources"
                @click="selectFromHistory">
                <span class="fa fa-database"></span>{{ btnHistoryTitle }}
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
import ArchiveTree from "./Archive/ArchiveTree";
import UploadBoxMixin from "./UploadBoxMixin";
import UploadRow from "mvc/upload/default/default-row";
import { BButton } from "bootstrap-vue";
import { uploadModelsToPayload } from "./helpers";

// We won't use an UploadRow as we only want to upload one archive at a time
// So we create a new component that will handle the archive contents?

// TODO: Handle/pass extensions tar, zip, bagit, yaml etc?
// These are hard-coded for now

const ARCHIVE_EXTENSIONS = [
    'tar',
    'zip',
    // 'yaml',    // yaml description? what is that?
];

export default {
    components: {
        BButton,
        ArchiveTree,
    },
    mixins: [UploadBoxMixin],
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
            multiple: false,
            rowUploadModel: UploadRow,
            archiveElements: {},
            counterAnnounce: 0,
            counterSuccess: 0,
            counterError: 0,
            counterRunning: 0,
            uploadSize: 0,
            uploadCompleted: 0,
            enableReset: false,
            enableStart: false,
            enableSources: false,
            highlightBox: false,
            btnLocalTitle: _l("Choose local file"),
            btnHistoryTitle: _l("Select from history"),
            btnCreateTitle: _l("Fetch remote file"),
            btnFtpTitle: _l("Choose FTP file"),
            btnStartTitle: _l("Start"),
            btnStopTitle: _l("Pause"),
            btnResetTitle: _l("Reset"),
        };
    },
    computed: {
        extensions() {
            return this.listExtensions.filter(
                (ext) => ARCHIVE_EXTENSIONS.includes(ext.id));
        },
        appModel() {
            // TODO: what does 'details' contain?
            return this.details.model;
        },
    },
    watch: {
        extension: function (value) {
            this.updateExtension(value);
        },
    },
    created() {
        this.initCollection();
        this.initAppProperties();
    },
    mounted() {
        this.initExtensionInfo();
        this.initFtpPopover();
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
            warning: (index, message) => {
                this._eventWarning(index, message);
            },
            error: (index, message) => {
                this._eventError(index, message);
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
    },
    methods: {
        _eventStart() {
/* There are a few different ways to go here...
Probably want to base action on current state

See UploadBoxMixin:_eventStart for parent method

~~ Local archive ~~
1 - Extract selected data from archive to temp data files on client
2 - Upload temp data files with standard API endpoints

~~ Remote archive ~~
Upload archive file with manifest to extract on server by either:
    1 - Extract and flatten entire archive to collection
    2 - Return archive manifest and allow user to select files to extract

*/
        },
        _eventStop() {

        },
        _eventReset() {

        },
        selectFromHistory() {
            // show "select from history" component
        }
    },
}
</script>
<style lang="">
    
</style>