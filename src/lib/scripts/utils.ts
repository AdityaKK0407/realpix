import { turnstile } from '$lib/state/turnstile.svelte';
import type { Colors, IconTypes } from '$lib/types/fileupload.types';

function range(start: number, end: number) {
	const array = [];
	for (let i = start; i < end; i++) {
		array.push(i);
	}
	return array;
}

function toTitleCase(stringVal: string) {
	const words = stringVal.split('');
	words[0] = words[0].toUpperCase();
	return words.join('');
}

function addSBasedOnCondition(condition: boolean, value: string) {
	return condition ? `${value}s` : value;
}

const utils = {
	returnColorForType: (type: IconTypes): Colors => {
		let color: Colors = null;
		switch (type) {
			case 'info':
				color = 'blue';
				break;

			case 'security-animated': {
				const turnstileStatus = turnstile.getStatus();
				if (turnstileStatus === 'verified') color = 'security-green';
				else if (turnstileStatus === 'error') color = 'red';
				else if (turnstileStatus === 'verifying') color = 'yellow';
				else if (turnstileStatus === 'manual-verification') color = 'periwinkle';
				else if (turnstileStatus === 'reset' || turnstileStatus === 'save-check') color = 'gray';
				break;
			}

			case 'security':
				color = 'green';
				break;
		}
		return color;
	},

	performAnimation(type: IconTypes) {
		let status = false;
		switch (type) {
			case 'security-animated':
				if (turnstile.getStatus() !== 'reset') status = true;
				break;
		}
		return status;
	}
};

export { range, toTitleCase, addSBasedOnCondition, utils };
