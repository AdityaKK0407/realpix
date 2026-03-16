import { PUBLIC_MAX_SIZE_OF_FILE } from '$env/static/public';

const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
const allowedExtensions = ['jpg', 'jpeg', 'png', 'webp'];

interface ReturnType {
	filteredFiles: File[];
	errorFileCount: number;
}

export function validateFiles(files: File[]): ReturnType {
	const MAX_LIMIT = 5;

	if (files.length > MAX_LIMIT) {
		files = files.slice(0, MAX_LIMIT);
	}

	const limit = parseInt(PUBLIC_MAX_SIZE_OF_FILE) * 1024 * 1024;

	let errorFileCount = 0;
	const filteredFiles = files.filter((file) => {
		if (file.size > limit) {
			errorFileCount++;
		} else {
			const splitArray = file.name.split('.');
			const ext = splitArray[splitArray.length - 1];
			if (!ext) {
				alert('error');
				return;
			}
			return allowedTypes.includes(file.type) && allowedExtensions.includes(ext.toLowerCase());
		}
	});

	return {
		filteredFiles,
		errorFileCount
	};
}
