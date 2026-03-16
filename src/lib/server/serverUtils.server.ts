import { MAX_BATCH_SIZE, MAX_SIZE_OF_FILE } from '$env/static/private';
import { json } from '@sveltejs/kit';

interface Data {
	task_ids: string[];
}

export type TotalPackageLimit = 's' | 'plm';
export type EachFileLimit = 's' | 'flm';

export const serverUtils = {
	max_package_size: parseInt(MAX_BATCH_SIZE) * 1024 * 1024,
	file_size_limit: parseInt(MAX_SIZE_OF_FILE) * 1024 * 1024,

	successResponse: (data: Data): Response => {
		return json({
			data: data
		});
	},

	errorResponse: (statusCode: number, statusMessage: string) => {
		return json(
			{
				data: null
			},
			{
				status: statusCode,
				statusText: statusMessage
			}
		);
	},

	checkPackageSizeSendStatus: function (image: File[]): TotalPackageLimit {
		let totalSize = 0;
		image.forEach((file) => (totalSize += file.size));

		return totalSize > this.max_package_size ? 'plm' : 's';
	},

	checkEachFileSizeStatus: function (image: File[]): EachFileLimit {
		let status: EachFileLimit = 's';
		for (const file of image) {
			if (file.size > this.file_size_limit) {
				status = 'flm';
				break;
			}
		}

		return status;
	}
};
