import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { PYTHON_BACKEND_SERVER } from '$env/static/private';
import z from 'zod';

const type = z.object({
	turnstileToken: z.string()
})

export const POST: RequestHandler = async ({ request, cookies }) => {
	try {
		const { turnstileToken } = await request.json();
		console.log(turnstileToken)
		const token = type.safeParse(turnstileToken);

		if(!token.success) {
			console.log('Provided data is in incorrect format or is missing')
			throw error(400, 'Error')
		}

		if (!turnstileToken) {
			throw error(400, 'Missing turnstile token');
		}

		const turnstileResponse = await fetch(`${PYTHON_BACKEND_SERVER}/verify/captcha`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				token: token.data?.turnstileToken
			})
		});

		const turnstileResult = await turnstileResponse.json();

		if (!turnstileResult.success) {
			throw error(401, 'Turnstile verification failed');
		}

		console.log('Turnstile verified');

		cookies.set('session_turnstile_token', turnstileResult.token, {
			httpOnly: true,
			secure: true,
			sameSite: 'strict',
			path: '/',
			maxAge: 86400000
		})

        return json({
            token: turnstileResult.token
        })
		
	} catch (err) {
		console.log('Error in verifying turnstile', err);
		throw error(500, 'Internal server error');
	}
};
