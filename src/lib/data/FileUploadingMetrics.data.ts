import type { MetricType } from '$lib/types/fileupload.types';
import { nanoid } from 'nanoid';

export const fileUploadFooterData: MetricType[] = [
	{
		id: nanoid(),
		icon: 'Ai',
		heading: 'Model',
		text: 'Real Pix V.1',
		iconType: 'info'
	},
	{
		id: nanoid(),
		icon: 'None',
		heading: 'Encryption',
		text: 'Active',
		iconType: 'security-animated'
	}
];
