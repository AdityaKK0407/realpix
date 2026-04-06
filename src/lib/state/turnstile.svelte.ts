export type TurnStile =
	| 'verifying'
	| 'verified'
	| 'error'
	| 'reset'
	| 'manual-verification'
	| 'save-check'
	| 'verification-timeout'
	| 'token-expired';

interface TurnstileStatus {
	status: TurnStile;
	token?: string;
	errorCode?: number;
}

export interface ErrorTurnstile {
	errorText: string | null;
	category: string | null;
	errorStatus: boolean;
}

import { browser } from '$app/environment';
import z from 'zod';

const statusType = z.object({
	status: z.boolean()
});

class Turnstile {
	private turnstileSetup: TurnStile;
	private turnstileToken: string;
	private turnstileStatusText: string;
	private autoCheckingStatus: boolean;
	private turnstileErrorText: string | null;
	private turnstileErrorCategory: string | null;

	constructor() {
		this.turnstileSetup = $state<TurnStile>('save-check');
		this.turnstileToken = '';
		this.turnstileStatusText = $state('Checking');
		this.autoCheckingStatus = true;
		this.turnstileErrorText = $state(null);
		this.turnstileErrorCategory = $state(null);
		this.init();
	}

	private async init() {
		if (browser) {
			const status = await this.checkTurnstile();
			if (!status) {
				this.turnstileSetup = 'reset';
				this.autoCheckingStatus = false;
			} else {
				this.turnstileSetup = 'verified';
			}
			this.changeStatusText();
		}
	}

	changeTurnstileStatus(arg: TurnstileStatus) {
		if (arg.status === 'verified' && arg.token) {
			this.turnstileToken = arg.token;
			this.verifyTurnstile();
		} else if (arg.status === 'error') {
			this.turnstileSetup = arg.status;
			if (!arg.errorCode) {
				throw Error('No Status Code Provided');
			}
			this.setTurnstileError(arg.errorCode);
		} else if (arg.status === 'verification-timeout') {
			if (!arg.errorCode) {
				throw Error('No Status Code Provided.');
			}
			this.turnstileSetup = arg.status;
			this.setTurnstileError(arg.errorCode);
		} else {
			this.turnstileSetup = arg.status;
			this.changeStatusText();
		}
	}

	private setTurnstileError(errorCode: number) {
		errorCode = Math.floor(errorCode / 1000);
		let message = '';
		let category = '';
		switch (errorCode) {
			case 100:
				message = 'Please refresh the page and try again.';
				category = 'Initilization problems.';
				break;
			case 102:
				message = 'Network or browser issues.';
				category = 'Invalid parameters (network).';
				break;
			case 103:
				message = 'Browser compatability issues.';
				category = 'Invalid parameters (browser).';
				break;
			case 104:
				message = 'Client validation failure.';
				category = 'Invalid parameters (client-side).';
				break;
			case 105:
				message = 'Implementation error.';
				category = 'API compatibility.';
				break;
			case 106:
				message = 'Parameters validation failures.';
				category = 'Invalid parameters (general).';
				break;
			case 110:
				message = 'Configuration error. Please contact support.';
				category = 'Configuration issues.';
				break;
			case 120:
				message = 'Connection Problems.';
				category = 'Network of loading issues.';
				break;
			case 200:
				message = 'Widget state problems.';
				category = 'Widget issues.';
				break;
			case 400:
				message = 'Invalid options.';
				category = 'Client configuration.';
				break;
			case 300:
			case 600:
				message = 'Security check failed. Please try refreshing or using a different browser.';
				category = 'Generic Challenge failure.';
				break;
			case 700:
				message = 'Challenge timed out. Please try again.';
				category = 'Time-Out';
				break;
			case 710:
				message = 'Token Expired. Resetting the widget.';
				category = 'Time-Out';
				break;
			default:
				message = 'An unexpected error occurred. Please try again.';
				break;
		}

		this.turnstileErrorText = message;
		this.turnstileErrorCategory = category;
	}

	async checkTurnstile(): Promise<boolean> {
		const ifExists = await fetch('/api/checkCookie');
		const ifExistsData = await ifExists.json();

		const result = statusType.safeParse(ifExistsData);
		if (!result.success) {
			return false;
		}
		return result.data.status;
	}

	getStatus() {
		return this.turnstileSetup;
	}

	shouldDisplay() {
		if (this.turnstileSetup === 'reset' && !this.autoCheckingStatus) {
			return true;
		} else {
			return false;
		}
	}

	private async verifyTurnstile() {
		console.log(this.turnstileToken);
		const verifyResponse = await fetch('/api/verify-turnstile', {
			headers: {
				'Content-Type': 'application/json'
			},
			method: 'POST',
			credentials: 'include',
			body: JSON.stringify({
				turnstileToken: this.turnstileToken
			})
		});

		if (verifyResponse.ok) {
			this.turnstileSetup = 'verified';
			this.changeStatusText();
		} else {
			this.turnstileSetup = 'error';
			this.changeStatusText();
		}
	}

	private changeStatusText() {
		let text = '';
		switch (this.turnstileSetup) {
			case 'reset':
				text = 'In-Active';
				break;

			case 'verifying':
				text = 'Verifying';
				break;

			case 'verified':
				text = 'Active';
				break;

			case 'error':
				text = 'Error';
				break;

			case 'manual-verification':
				text = 'Attention';
				break;
		}
		this.turnstileStatusText = text;
	}

	getStatusInfo() {
		return this.turnstileStatusText;
	}

	getErrorStatus() {
		return {
			errorText: this.turnstileErrorText,
			category: this.turnstileErrorCategory,
			errorStatus: true
		};
	}
}

export const turnstile = new Turnstile();
