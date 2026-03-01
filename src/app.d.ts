// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
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
					'error-callback': (error: Error) => void;
					'render-callback': () => void
					'before-interaction': () => void;
					'tiemout-callback': () => void;
				}
			) => string | undefined;
			remove: (widgetId: string) => void;
		};
	}
}

export {};
