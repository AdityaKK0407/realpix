import { writable} from 'svelte/store';

export const uploadedFiles = writable<File[]>([])