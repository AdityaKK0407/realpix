declare module '$env/static/private' {
	export const MAX_BATCH_SIZE: string;
	export const MAX_SIZE_OF_FILE: string;
	export const PYTHON_BACKEND_SERVER: string;
}

declare module '$env/static/public' {
	export const PUBLIC_BASE_TIME_REQUEST: string;
	export const PUBLIC_MAX_BATCH_SIZE: string;
	export const PUBLIC_MAX_SIZE_OF_FILE: string;
	export const PUBLIC_REQUEST_BIAS: string;
	export const PUBLIC_TURNSTILE_SITE_KEY: string;
	export const PUBLIC_WEBSITE_URL: string;
}
