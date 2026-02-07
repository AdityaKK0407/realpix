import { nanoid } from 'nanoid';

export const fileUploadFooterData = [
	{
		id: nanoid(),
		icon: 'Sparkles',
		heading: 'Model',
		text: 'Real Pix V.1',
		color: 'blue'
	},
	{
		id: nanoid(),
		icon: 'Shield',
		heading: 'Encryption',
		text: 'Active',
		color: 'green'
	}
] as const;
