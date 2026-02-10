import { get, writable } from 'svelte/store';
import { nanoid } from 'nanoid';

export interface FileUploader {
	id: string
	type: 'image' | 'video'
	src: File
	blob: string
	name: string
}

export type FileType = 'image' | 'video'

export const uploadedFiles = writable<FileUploader[]>([])

function uploadFiles(newFiles: File[], fileType: FileType) {
	const newItems: FileUploader[] = newFiles.map((file: File) => {
		return {
			id: nanoid(),
			type: fileType,
			src: file,
			blob: URL.createObjectURL(file),
			name: file.name
		};
	});
	uploadedFiles.update((file) => [...file, ...newItems]);
}

function returnFileUploader() {
	return get(uploadedFiles);
}

function returnFileType(fileType: FileType) {
	const files = returnFileUploader()
	return files.filter((file: FileUploader) => file.type === fileType)
}

function returnBlobs(fileType: FileType) {
	const fileTypeFiles = returnFileType(fileType);
	return fileTypeFiles.map((file: FileUploader) => file.blob)
}

function returnLength(fileType: FileType) {
	return returnFileType(fileType).length;
}

function returnLengthOne(fileType: FileType) {
	return returnFileType(fileType).length === 1;
}

function getNamesOfType(fileType: FileType) {
	const files = returnFileType(fileType);
	return files.map((file: FileUploader) => file.name)
}

function clearData() {
	uploadedFiles.set([]);
}

export { uploadFiles, returnFileType, returnLength, returnBlobs, returnFileUploader, clearData, returnLengthOne, getNamesOfType };