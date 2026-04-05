import type { RequestHandler } from './$types';
import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import z from 'zod';
import { serverUtils } from '$lib/server/serverUtils.server';

const turnstileTokenType = z.object({
	turnstileToken: z.string().min(1)
});

const SERVERVALIDRESPONSE = z.object({
	status: z.literal('success'),
	user_token: z.string()
});

const SERVERINVALIDRESPONSE = z.object({
	status: z.literal('error'),
	detail: z.string()
});

const SERVERRESPONSE = z.discriminatedUnion('status', [SERVERVALIDRESPONSE, SERVERINVALIDRESPONSE]);

export const POST: RequestHandler = async ({ request, cookies, getClientAddress }) => {
	const turnstileResponse = await request.json();
	const token = turnstileTokenType.safeParse(turnstileResponse);

	if (!token.success) {
		return serverUtils.errorResponse(400, 'Provided data is in incorrect format or is missing');
	}

	const serverTokenResponse = await fetch(`${PYTHON_BACKEND_SERVER}/verify/captcha`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-Client-Ip': getClientAddress()
		},
		body: JSON.stringify({
			token: token.data.turnstileToken
		})
	});

	const serverTokenJSONResponse = await serverTokenResponse.json();
	const parsedResponse = SERVERRESPONSE.safeParse(serverTokenJSONResponse);

	if (!parsedResponse.success) {
		return serverUtils.errorResponse(500, 'Failed to parse backend response');
	}

	if (!serverTokenResponse.ok && parsedResponse.data?.status === 'error') {
		return serverUtils.errorResponse(serverTokenResponse.status, parsedResponse.data.detail);
	}

	if (parsedResponse.data.status === 'success') {
		cookies.set('session_turnstile_token', parsedResponse.data.user_token, {
			httpOnly: true,
			secure: true,
			sameSite: 'strict',
			path: '/',
			maxAge: 86400
		});

		return serverUtils.successResponse({
			token: parsedResponse.data.user_token
		});
	} else {
		return serverUtils.errorResponse(500, 'Internal Server Error');
	}
};
