import type { UploadEvent, UploadState } from '$lib/upload/upload.types';

export const uploadTransition: Record<UploadState, Partial<Record<UploadEvent, UploadState>>> = {
	idle: {
		SELECT_IMAGE: 'ready'
	},
	ready: {
		START_UPLOAD: 'processing',
		RESET: 'idle'
	},
	processing: {
		ANALYSIS_SUCCESS: 'result'
	},
	result: {
		RESET: 'idle'
	},
	error: {
		RESET: 'idle'
	}
};
