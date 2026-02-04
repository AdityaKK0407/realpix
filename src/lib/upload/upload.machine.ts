import type { UploadEvent, UploadState } from '$lib/upload/upload.types';

export const uploadTransition : Record<UploadState, Partial<Record<UploadEvent, UploadState>>> = {
	idle: {
		SELECT_IMAGE: 'ready'
	},
	ready: {
		START_UPLOAD: 'uploading',
		RESET: 'idle'
	},
	uploading: {
		UPLOAD_SUCCESS: "analyzing",
		UPLOAD_FAILURE: 'error'
	},
	analyzing: {
		 ANALYSIS_SUCCESS: 'result'
	},
	result: {
		RESET: 'idle'
	},
	error: {
		RESET: 'idle'
	}
}