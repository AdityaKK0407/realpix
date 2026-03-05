import type { Cookies, Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve}) => {
    const { url, cookies } = event;

    const publicRoutes = [
        '/api/health'
    ]

    const isPublicRoute = publicRoutes.some(route => url.pathname.startsWith(route));
    const sessionToken = cookies.get('session_turnstile_token');

    if(isPublicRoute || !sessionToken) {
        event.locals.turnstileSessionToken = null;
        return resolve(event);
    }

    event.locals.turnstileSessionToken = sessionToken;
    return resolve(event)
}