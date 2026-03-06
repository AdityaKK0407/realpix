// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			turnstileSessionToken: string | null;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	interface Window {
		turnstile: {
			render: (
				container: string | HTMLElement,
				params: {
					sitekey: string;
					callback?: (token: string) => void;
					theme?: 'light' | 'dark';
					size?: 'normal' | 'compact';
					'error-callback': (error: number) => void;
					'before-interactive-callback': () => void;
					'timeout-callback': () => void;
					'expired-callback': () => void;
					retry: 'auto' | 'never';
					'retry-interval': number;
				}
			) => string | undefined;
			remove: (widgetId: string) => void;
			reset: (widgetId: string) => void;
		};
	}
}

export {};
