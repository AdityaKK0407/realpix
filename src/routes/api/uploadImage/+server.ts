import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { type RequestHandler } from '@sveltejs/kit';
import z from 'zod';
import { serverUtils, type EachFileLimit, type TotalPackageLimit } from '$lib/server/serverUtils.server';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		return serverUtils.errorResponse(401, 'Not authenticated. Please authenticated to continue.');
	}

	const uploadImageSuccessResponseType = z.object({
		task_ids: z.array(z.string()).max(5).min(1)
	});

	const uploadImageErrorResponseType = z.object({
		detail: z.string()
	});

	const uploadImageResponseType = z.union([
		uploadImageErrorResponseType,
		uploadImageSuccessResponseType
	]);

	const formData = await request.formData();
	const imageFiles = formData.getAll('images') as File[];
	
	const packageCheck: TotalPackageLimit = serverUtils.checkPackageSizeSendStatus(imageFiles);
	const eachFileCheck: EachFileLimit = serverUtils.checkEachFileSizeStatus(imageFiles)

	if(packageCheck === 'plm' || eachFileCheck === 'flm') {
		return serverUtils.errorResponse(413, 'PayLoad Too large');
	}

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

	// Use 'in' operator to check which part of the union was matched
	if ('task_ids' in uploadState.data) {
		return serverUtils.successResponse({
			task_ids: uploadState.data.task_ids
		});
	} else {
		return serverUtils.errorResponse(response.status, uploadState.data.detail);
	}
};
