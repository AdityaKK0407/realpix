import type { UploadState, UploadEvent } from '$lib/upload/upload.types';
import { uploadTransition } from '$lib/upload/upload.machine';

class MainState {
	private uploadState: UploadState;

	constructor() {
		this.uploadState = $state('idle');
	}

	transitionState(event: UploadEvent) {
		const current = this.uploadState;
		const next = uploadTransition[current]?.[event];
		if (!next) {
			alert('error occurred');
			return;
		}
		this.uploadState = next;
	}

	getUploadState() {
		return this.uploadState;
	}
}

const mainState = new MainState();

export { mainState };
