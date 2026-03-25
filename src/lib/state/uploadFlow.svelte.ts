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
export type UploadType = {
	formData: FormData | undefined;
	batchId: string[] | undefined;
};

class UploadState {
	private imageFiles: FileUploader[];
	private videoFiles: FileUploader[];
	imageLength: number;
	videoLength: number;
	MAX_LENGTH: number = 5;
	MAX_BATCH_SIZE: number = parseInt(PUBLIC_MAX_BATCH_SIZE) * 1024 * 1024;
	batchedFiles: string[];

	constructor() {
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
				const newJoinedFiles = [...this.imageFiles, ...newItems];
				this.imageFiles = newJoinedFiles;
			} else if (fileType === 'video') {
				this.videoLength += newFiles.length;
				const newJoinedFiles = [...this.videoFiles, ...newItems];
				this.videoFiles = newJoinedFiles;
			}
		}
	}

	getFilesByType(fileType: FileType) {
		if (browser) {
			return fileType === 'image' ? this.imageFiles : this.videoFiles;
		}
	}

	getBlobs(fileType: FileType) {
		const files = this.getFilesByType(fileType);
		return files && files.map((file: FileUploader) => file.blob);
	}

	getName(id: string, fileType: FileType) {
		return this.getFile(id, fileType)?.name;
	}

	getFile(id: string, fileType: FileType) {
		const files = fileType === 'image' ? this.imageFiles : this.videoFiles;
		return files.find((file: FileUploader) => file.id === id);
	}

	getFileBlob(id: string, fileType: FileType) {
		const file = this.getFile(id, fileType);
		if (file) {
			return file.blob;
		} else {
			return this.getFilesTypeFirstBlob(fileType);
		}
	}

	getFilesTypeFirstBlob(fileType: FileType) {
		const files = this.getFilesByType(fileType);
		return files && files[0].blob;
	}

	getFileTypeFirstId(fileType: FileType) {
		const files = this.getFilesByType(fileType);
		return files && files[0].id;
	}

	getLength(fileType: FileType) {
		return fileType === 'image' ? this.imageLength : this.videoLength;
	}

	getMaxLength() {
		return this.MAX_LENGTH;
	}

	clearItems() {
		this.imageFiles.forEach((file) => {
			URL.revokeObjectURL(file.blob);
		});
		this.videoFiles.forEach((file) => {
			URL.revokeObjectURL(file.blob);
		});
		this.imageFiles = [];
		this.videoFiles = [];
		this.imageLength = 0;
		this.videoLength = 0;
	}

	private generateBatch(fileType: FileType) {
		const batchToSend: File[] = [];
		let notBatched = 0;
		let sizeOfBatch = 0;
		const filesToSend = this.getFilesByType(fileType);
		const batchIds = [];

		if (filesToSend) {
			for (const file of filesToSend) {
				if (file.size + sizeOfBatch > this.MAX_BATCH_SIZE) {
					notBatched++;
					break;
				} else {
					if (!this.batchedFiles.includes(file.id)) {
						batchToSend.push(file.src);
						sizeOfBatch += file.size;
						this.batchedFiles.push(file.id);
						batchIds.push(file.id);
					}
				}
			}

			return {
				batchFiles: batchToSend,
				batchIds,
				noOfNotBatched: notBatched
			};
		}
	}

	private generateFormData(fileType: FileType) {
		const dataToSend = this.generateBatch(fileType);
		if (dataToSend) {
			const { batchFiles, noOfNotBatched, batchIds } = dataToSend;
			const formData = new FormData();
			batchFiles.forEach((data) => {
				formData.append(`${fileType}s`, data);
			});

			return {
				noOfNotBatched,
				formData,
				batchIds
			};
		} else {
			return undefined;
		}
	}

	createPackageObject(formData: FormData | undefined, batchIds: string[] | undefined): UploadType {
		return {
			formData,
			batchId: batchIds
		};
	}

	createPackages(fileType: FileType) {
		const package1 = this.generateFormData(fileType);
		if (package1) {
			let package2;
			let moreBatchAvailable: boolean;
			if (package1.noOfNotBatched > 0) {
				package2 = this.generateFormData(fileType);
				if (package2) {
					moreBatchAvailable = package2.noOfNotBatched > 0;
				} else {
					moreBatchAvailable = false;
				}
			} else {
				moreBatchAvailable = false;
			}

			return {
				sendData: [
					this.createPackageObject(package1.formData, package1.batchIds),
					this.createPackageObject(package2?.formData, package2?.batchIds)
				],
				package1FormData: package1.formData,
				package1BatchIds: package1.batchIds,
				package2FormData: package2?.formData,
				package2BatchIds: package2?.batchIds,
				moreBatchAvailable
			};
		}
	}

	createCustomPackages() {}
}

const uploadData = new UploadState();

export { uploadData };
