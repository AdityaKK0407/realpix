const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
const allowedExtensions = ['jpg', 'jpeg', 'png', 'webp'];

export function validateFiles(files: File[]): File[] {
	return files.filter((file) => {
		const splitArray = file.name.split('.');
		const ext = splitArray[splitArray.length - 1];
		if (!ext) {
			alert('error');
			return;
		}
		return allowedTypes.includes(file.type) && allowedExtensions.includes(ext.toLowerCase());
	});
}
