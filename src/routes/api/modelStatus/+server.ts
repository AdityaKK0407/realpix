import type { RequestHandler } from './$types';
import { serverUtils } from '$lib/server/serverUtils.server';
import z from 'zod';
import { PYTHON_BACKEND_SERVER } from '$env/static/private';

const requestType = z.object({
	task_id: z.string()
});

const RESPONSEERRORTYPE = z.object({
	status: z.literal('error'),
	detail: z.string()
});

const SUCCESSRESPONSECOMPLETEDRESULT = z.object({
	status: z.literal('success'),
	result: z.literal('completed'),
	data: z.array(z.boolean())
});

const SUCCESSRESPONSEFAILEDRESULT = z.object({
	status: z.literal('success'),
	result: z.literal('failed')
});

const SUCCESSRESPONSEPENDINGRESULT = z.object({
	status: z.literal('success'),
	result: z.literal('pending')
});

const RESPONSETYPE = z.discriminatedUnion('status', [
	RESPONSEERRORTYPE,
	z.discriminatedUnion('result', [
		SUCCESSRESPONSECOMPLETEDRESULT,
		SUCCESSRESPONSEFAILEDRESULT,
		SUCCESSRESPONSEPENDINGRESULT
	])
]);

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.turnstileSessionToken) {
		return serverUtils.errorResponse(401, 'Not authenticated. Please');
	}
	const data = await request.json();

	const requestParse = requestType.safeParse(data);
	if (!requestParse.success) {
		return serverUtils.errorResponse(500, 'Incompatible result type');
	}

	const response = await fetch(
		`${PYTHON_BACKEND_SERVER}/model/status/${requestParse.data.task_id}`
	);
};
