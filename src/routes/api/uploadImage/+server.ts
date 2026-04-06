import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import { type RequestHandler } from '@sveltejs/kit';
import z from 'zod';
import {
	serverUtils,
	type EachFileLimit,
	type TotalPackageLimit
} from '$lib/server/serverUtils.server';

const UPLOADSUCCESSTYPE = z.object({
	status: z.literal('success'),
	task_id: z.string()
});

const UPLOADERRORTYPE = z.object({
	status: z.literal('error'),
	detail: z.string()
});

const UPLOADTYPE = z.discriminatedUnion('status', [UPLOADSUCCESSTYPE, UPLOADERRORTYPE]);

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		return serverUtils.errorResponse(401, 'Not authenticated. Please authenticate to continue.');
	}

	const formData = await request.formData();
	const imageFiles = formData.getAll('images') as File[];

	const packageCheck: TotalPackageLimit = serverUtils.checkPackageSizeSendStatus(imageFiles);
	const eachFileCheck: EachFileLimit = serverUtils.checkEachFileSizeStatus(imageFiles);

	if (packageCheck === 'plm' || eachFileCheck === 'flm') {
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
	console.log(responseResult);

	const uploadState = UPLOADTYPE.safeParse(responseResult);
	if (!uploadState.success) {
		return serverUtils.errorResponse(500, 'Incompatible result type');
	}

	if (uploadState.data.status === 'success') {
		return serverUtils.successResponse({
			task_ids: uploadState.data.task_id
		});
	}

	if (uploadState.data.status === 'error') {
		return serverUtils.errorResponse(response.status, uploadState.data.detail);
	} else {
		return serverUtils.errorResponse(500, 'Internal server Error');
	}
};
