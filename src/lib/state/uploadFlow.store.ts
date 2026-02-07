import { writable} from 'svelte/store';

export interface FileUploader {
	id: string
	type: 'image' | 'video'
	src: File
}

export const uploadedFiles = writable<FileUploader[]>([])