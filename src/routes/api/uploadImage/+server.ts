import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { error, json, type RequestHandler } from '@sveltejs/kit';
import z from 'zod';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		throw error(401, 'Not authenticated');
	}

	const uploadImageSuccessResponseType = z.object({
		task_ids: z.array(z.string()).max(5).min(1),
	});

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

	if (!response.ok) {
		throw error(response.status, response.statusText);
	}

	const responseResult = await response.json();

	const uploadState = uploadImageSuccessResponseType.safeParse(responseResult);
		if (!uploadState.success) {
			throw error(500, 'Incompatible result type.');
		}

		return json({
			task_ids: uploadState.data.task_ids,
			status: response.status
		});
};
