import { get, writable, type Writable } from 'svelte/store';
import { nanoid } from 'nanoid';
import { files } from '$service-worker';

export interface FileUploader {
	id: string
	type: 'image' | 'video'
	src: File
	blob: string
	name: string
}

export type FileType = 'image' | 'video'

class UploadState {
	uploadFilesWritable: Writable<FileUploader[]>
	imageLength: number
	videoLength: number
	uploadedFiles: FileUploader[]
	MAX_LENGTH: number = 5

	constructor() {
		this.uploadFilesWritable = writable<FileUploader[]>([])
		this.imageLength = 0;
		this.videoLength = 0;
		this.uploadedFiles = [];
	}

	uploadFiles(newFiles: File[], fileType: FileType) {
		if (fileType === 'image') {
			this.imageLength += newFiles.length
		} else if (fileType === 'video') {
			this.videoLength += newFiles.length
		}

		const newItems: FileUploader[] = newFiles.map((file: File) => {
			return {
				id: nanoid(),
				type: fileType,
				src: file,
				blob: URL.createObjectURL(file),
				name: file.name
			};
		});
		this.uploadFilesWritable.update((file) => [...file, ...newItems]);
		this.uploadedFiles = get(this.uploadFilesWritable);
	}

	getFileType(fileType: FileType) {
		return this.uploadedFiles.filter((file: FileUploader) => file.type === fileType)
	}

	getBlobs(fileType: FileType) {
		const files = this.getFileType(fileType)
		return files.map((file: FileUploader) => file.blob)
	}

	getNamesOfType(fileType: FileType) {
		const files = this.getFileType(fileType);
		return files.map((file: FileUploader) => file.name)
	}

	getName(id: string) {
		return this.getFile(id)?.name
	}

	getFile(id: string) {
		return this.uploadedFiles.find((file: FileUploader) => file.id === id)
	}

	getFileBlob(id: string) {
		const file = this.getFile(id)
		if(file) {
			return file.blob;
		} else {
			return this.uploadedFiles[0].blob
		}
	}

	getFileTypeFirstId(fileType: FileType) {
		const files = this.getFileType(fileType)
		return files[0].id
	}

	getLength(fileType: FileType) {
		return fileType === 'image' ? this.imageLength : this.videoLength;
	}

	getMaxLength() {
		return this.MAX_LENGTH;
	}

	clearItems() {
		this.uploadFilesWritable.set([])
		this.imageLength = 0;
		this.videoLength = 0;
		this.uploadedFiles = []
	}
}

const uploadData = new UploadState();

export { uploadData }