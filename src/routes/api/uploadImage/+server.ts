import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { error, json, type RequestHandler } from '@sveltejs/kit';
import axios from 'axios';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		throw error(401, 'Not authenticated');
	}

	const formData = await request.formData();
    console.log(typeof formData)
    console.log(formData)

	const response = await axios(`${PYTHON_BACKEND_SERVER}/model/images`, {
		method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data',
            'X-RateLimit-Token': locals.turnstileSessionToken
        },
        data: formData
	});

    console.log(response)
    console.log(response.data.detail)

	return json({
		data: response
	});
};
