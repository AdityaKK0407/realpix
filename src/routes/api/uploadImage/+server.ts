import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { type RequestHandler } from '@sveltejs/kit';
import z from 'zod';
import { serverUtils } from '$lib/server/response.server';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		return serverUtils.errorResponse(401, 'Not authenticated. Please authenticated to continue.');
	}

	const uploadImageSuccessResponseType = z.object({
		status: z.literal("success"),
		task_ids: z.array(z.string()).max(5).min(1)
	});

	const uploadImageErrorResponseType = z.object({
		status: z.literal("error"),
		detail: z.string()
	});

	const uploadImageResponseType = z.discriminatedUnion('detail', [
		uploadImageSuccessResponseType,
		uploadImageErrorResponseType
	]);

	const formData = await request.formData();

	// 	Axios currently not supported in netlify production mode. So default fetch api is being used.
	// 	response = await axios(`${PYTHON_BACKEND_SERVER}/model/images`, {
	// 		method: 'POST',
	// 		headers: {
	// 			'X-RateLimit-Token': locals.turnstileSessionToken
	// 		},
	// 		data: formData
	// 	});
	// 	const uploadState = uploadImageSuccessResponseType.safeParse(response.data);
	// 	if (!uploadState.success) {
	// 		throw error(500, 'Incompatible result type.');
	// 	}
	//
	// 	return json({
	// 		data: response.data
	// 	});

	const response = await fetch(`${PYTHON_BACKEND_SERVER}/model/images`, {
		method: 'POST',
		headers: {
			'X-RateLimit-Token': locals.turnstileSessionToken
		},
		body: formData
	});

	const responseResult = await response.json();

	const uploadState = uploadImageResponseType.safeParse(responseResult);
	if (!uploadState.success) {
		return serverUtils.errorResponse(500, 'Incompatible result type');
	}

	if (uploadState.data.status === "success") {
		console.log('hi')
		return serverUtils.successResponse(
			{
				task_ids: uploadState.data.task_ids
			},
			response.status
		);
	} else {
		return serverUtils.errorResponse(response.status, uploadState.data.detail);
	}
};
