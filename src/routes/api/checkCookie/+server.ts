import { browser } from '$app/environment';
import { type Cookies, json, type RequestHandler } from '@sveltejs/kit';

interface Requirements {
	cookies: Cookies;
}

export const GET: RequestHandler = ({ cookies }: Requirements) => {
    if(browser) {
        const ifExists = cookies.get('turnstile-token');
        return json({
            status: ifExists ? true : false
        });
    }
};
