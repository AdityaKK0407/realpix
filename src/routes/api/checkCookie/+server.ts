import { type Cookies, json, type RequestHandler } from '@sveltejs/kit';

interface Requirements {
	cookies: Cookies;
}

export const GET: RequestHandler = ({ cookies }: Requirements) => {
	const ifExists = cookies.get('session_turnstile_token');
	return json({
		status: !!ifExists
	});
};
