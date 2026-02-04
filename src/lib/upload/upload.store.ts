import type { UploadState, UploadEvent} from '$lib/upload/upload.types';
import { uploadTransition } from '$lib/upload/upload.machine';
import { writable, get} from 'svelte/store';

export const uploadState = writable<UploadState>('idle')

export function transition(event: UploadEvent) {
	const current = get(uploadState);
	const next = uploadTransition[current]?.[event]
	if(!next) {
		alert('error occurred')
		return
	}
	uploadState.set(next)
}