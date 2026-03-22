import { nanoid } from 'nanoid';
import { browser } from '$app/environment';
import { PUBLIC_MAX_BATCH_SIZE } from '$env/static/public';

export interface FileUploader {
	id: string;
	type: 'image' | 'video';
	src: File;
	blob: string;
	name: string;
	size: number;
}

export type FileType = 'image' | 'video';

class UploadState {
	uploadedFiles: FileUploader[];
	imageFiles: FileUploader[];
	videoFiles: FileUploader[];
	imageLength: number;
	videoLength: number;
	MAX_LENGTH: number = 5;
	MAX_BATCH_SIZE: number = parseInt(PUBLIC_MAX_BATCH_SIZE) * 1024 * 1024;
	batchedFiles: string[];

	constructor() {
		this.uploadedFiles = $state<FileUploader[]>([]);
		this.imageFiles = $state<FileUploader[]>([]);
		this.videoFiles = $state<FileUploader[]>([]);
		this.imageLength = 0;
		this.videoLength = 0;
		this.batchedFiles = [];
	}

	uploadFiles(newFiles: File[], fileType: FileType) {
		if (browser) {
			const newItems: FileUploader[] = newFiles.map((file: File) => {
				return {
					id: nanoid(),
					type: fileType,
					src: file,
					blob: URL.createObjectURL(file),
					name: file.name,
					size: file.size
				};
			});

			if (fileType === 'image') {
				this.imageLength += newItems.length;
				const newFiles = [...this.imageFiles, ...newItems]
			} else if (fileType === 'video') {
				this.videoLength += newFiles.length;
			}

			const newUploadedFiles = [...this.uploadedFiles, ...newItems];
			this.uploadedFiles = newUploadedFiles;
		}
	}

	getFileType(fileType: FileType) {
		return browser
			? this.uploadedFiles.filter((file: FileUploader) => file.type === fileType)
			: undefined;
	}

	getBlobs(fileType: FileType) {
		const files = this.getFileType(fileType);
		return files && files.map((file: FileUploader) => file.blob);
	}

	getNamesOfType(fileType: FileType) {
		const files = this.getFileType(fileType);
		return files && files.map((file: FileUploader) => file.name);
	}

	getName(id: string) {
		return this.getFile(id)?.name;
	}

	getFile(id: string) {
		return this.uploadedFiles.find((file: FileUploader) => file.id === id);
	}

	getFileBlob(id: string) {
		const file = this.getFile(id);
		if (file) {
			return file.blob;
		} else {
			return this.uploadedFiles[0].blob;
		}
	}

	getFileTypeFirstId(fileType: FileType) {
		const files = this.getFileType(fileType);
		return files && files[0].id;
	}

	getLength(fileType: FileType) {
		return fileType === 'image' ? this.imageLength : this.videoLength;
	}

	getMaxLength() {
		return this.MAX_LENGTH;
	}

	clearItems() {
		this.uploadedFiles = [];
		this.imageLength = 0;
		this.videoLength = 0;
	}

	private generateBatch() {
		const batchToSend: File[] = [];
		let notBatched = 0;
		let sizeOfBatch = 0;

		for (const file of this.uploadedFiles) {
			if (file.size + sizeOfBatch > this.MAX_BATCH_SIZE) {
				notBatched++;
				break;
			} else {
				if (!this.batchedFiles.includes(file.id)) {
					batchToSend.push(file.src);
					sizeOfBatch += file.size;
					this.batchedFiles.push(file.id);
				}
			}
		}

		return {
			batchFiles: batchToSend,
			noOfNotBatched: notBatched
		};
	}

	private generateFormData(fileType: FileType) {
		const { batchFiles, noOfNotBatched } = this.generateBatch();
		const formData = new FormData();
		batchFiles.forEach((data) => {
			formData.append(`${fileType}s`, data);
		});

		return {
			noOfNotBatched,
			formData
		};
	}

	createPackages(fileType: FileType) {
		const package1 = this.generateFormData(fileType);
		let package2;
		let moreBatchAvailable: boolean;
		if (package1.noOfNotBatched > 0) {
			package2 = this.generateFormData(fileType);
			moreBatchAvailable = package2.noOfNotBatched > 0;
		} else {
			moreBatchAvailable = false;
		}

		return {
			package1: package1.formData,
			package2: package2?.formData,
			moreBatchAvailable
		};
	}

	createCustomPackages() {}
}

const uploadData = new UploadState();

export { uploadData };
