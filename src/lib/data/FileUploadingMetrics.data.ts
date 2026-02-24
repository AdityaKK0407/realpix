import type { MetricType } from '$lib/types/fileupload.types';
import { nanoid } from 'nanoid';

export const fileUploadFooterData: MetricType[] = [
	{
		id: nanoid(),
		icon: 'Ai',
		heading: 'Model',
		text: 'Real Pix V.1',
		color: 'blue'
	},
	{
		id: nanoid(),
		icon: 'Shield',
		heading: 'Encryption',
		text: 'Active',
		color: 'green',
		turnstileSupport: true
	}
];
