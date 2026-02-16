export type UploadState = 'idle' | 'ready' | 'uploading' | 'analyzing' | 'result' | 'error';

export type UploadEvent =
	| 'SELECT_IMAGE'
	| 'START_UPLOAD'
	| 'UPLOAD_SUCCESS'
	| 'UPLOAD_FAILURE'
	| 'ANALYSIS_SUCCESS'
	| 'RESET';
