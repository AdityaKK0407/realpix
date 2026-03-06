const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
const allowedExtensions = ['jpg', 'jpeg', 'png', 'webp'];

interface ReturnType {
	filteredFiles: File[];
}

export function validateFiles(files: File[]): ReturnType {
	const MAX_LIMIT = 5;

	if (files.length > MAX_LIMIT) {
		files = files.slice(0, MAX_LIMIT);
	}

	return {
		filteredFiles: files.filter((file) => {
			const splitArray = file.name.split('.');
			const ext = splitArray[splitArray.length - 1];
			if (!ext) {
				alert('error');
				return;
			}
			return allowedTypes.includes(file.type) && allowedExtensions.includes(ext.toLowerCase());
		})
	};
}
