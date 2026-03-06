import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { error, json, type RequestHandler } from '@sveltejs/kit';
import axios from 'axios';
import z from 'zod';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		throw error(401, 'Not authenticated');
	}

	const uploadImageSuccessResponseType = z.object({
		task_ids: z.array(z.string()).max(5).min(1)
	});

	const formData = await request.formData();

	const response = await axios(`${PYTHON_BACKEND_SERVER}/model/images`, {
		method: 'POST',
		headers: {
			'Content-Type': 'multipart/form-data',
			'X-RateLimit-Token': locals.turnstileSessionToken
		},
		data: formData
	});

	const uploadState = uploadImageSuccessResponseType.safeParse(response.data);
	if (!uploadState.success) {
		throw error(500, 'Incompatiable result type.');
	}

	return json({
		data: response.data
	});
};
