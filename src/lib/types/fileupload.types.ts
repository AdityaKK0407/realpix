export type FileUploadOptions = 'resetState' | 'draggingState' | 'errorState' | 'successState';

export type IconNames = 'Ai' | 'Shield' | 'Server';
export type Colors = 'blue' | 'green' | 'orange';

export interface MetricType {
	id: string;
	icon: IconNames;
	heading: string;
	text: string;
	color: Colors;
	turnstileSupport?: boolean;
}
