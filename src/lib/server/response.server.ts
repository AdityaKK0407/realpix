import { json } from '@sveltejs/kit';

interface Data {
	task_ids?: string[];
}

export const serverUtils = {
	successResponse: (data: Data, statusCode: number): Response => {
		return json({
			data: data,
			status: statusCode,
			errorMessage: null
		});
	},

	errorResponse: (statusCode: number, statusMessage: string) => {
		return json({
			data: null,
			status: statusCode,
			errorMessage: statusMessage
		});
	}
};

console.log('hi');
