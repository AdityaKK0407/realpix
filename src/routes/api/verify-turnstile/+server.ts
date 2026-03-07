import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import z from 'zod';

const turnstileTokenType = z.object({
	turnstileToken: z.string().min(1)
});

export const POST: RequestHandler = async ({ request, cookies, getClientAddress }) => {
	const turnstileResponse = await request.json();
	const token = turnstileTokenType.safeParse(turnstileResponse);

	if (!token.success) {
		throw error(400, 'Provided data is in incorrect format or is missing');
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

	if (!serverTokenResponse.ok) {
		throw error(serverTokenResponse.status, serverTokenResponse.statusText);
	}

	const serverTokenJSONResponse = await serverTokenResponse.json();

	const serverResponseType = z.object({
		user_token: z.string()
	});

	const parsedBackendToken = serverResponseType.safeParse(serverTokenJSONResponse);

	if (!parsedBackendToken.success) {
		throw error(500, 'Failed to parse backend response');
	}

	cookies.set('session_turnstile_token', parsedBackendToken.data.user_token, {
		httpOnly: true,
		secure: true,
		sameSite: 'strict',
		path: '/',
		maxAge: 86400
	});

	return json({
		token: parsedBackendToken.data.user_token
	});
};
