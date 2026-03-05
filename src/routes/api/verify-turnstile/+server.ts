import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import z from 'zod';
import axios from 'axios';

const turnstileTokenType = z.object({
	turnstileToken: z.string().min(1)
})

export const POST: RequestHandler = async ({ request, cookies }) => {
	try {
		const turnstileResponse = await request.json();
		const token = turnstileTokenType.safeParse(turnstileResponse);

		if(!token.success) {
			console.log('Provided data is in incorrect format or is missing')
			throw error(400, 'Error')
		}

		const serverTokenResponse = await axios(`${PYTHON_BACKEND_SERVER}/verify/captcha`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			data: {
				token: token.data.turnstileToken
			}
		});

		const serverResponseType = z.object({
			user_token: z.string()
		})

		const parsedBackendToken = serverResponseType.safeParse(serverTokenResponse.data);

		if (!parsedBackendToken.success) {
			throw error(500, 'Failed to parse backend response')
		}

		cookies.set('session_turnstile_token', parsedBackendToken.data.user_token, {
			httpOnly: true,
			secure: true,
			sameSite: 'strict',
			path: '/',
			maxAge: 86400
		})

        return json({
            token: parsedBackendToken.data.user_token
        })
		
	} catch (err) {
		console.log('Error in verifying turnstile', err);
		throw error(500, 'Internal server error');
	}
};
