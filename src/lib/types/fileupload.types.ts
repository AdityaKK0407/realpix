export type FileUploadOptions = 'resetState' | 'draggingState' | 'errorState' | 'successState';

export type IconNames = 'Ai' | 'Shield' | 'Server' | 'None';
export type IconTypes = 'security' | 'security-animated' | 'info'
export type Colors = 'yellow' | 'red' | 'periwinkle' | 'gray' | 'security-green' | 'green' | 'blue' | null

export interface MetricType {
	id: string;
	icon: IconNames;
	heading: string;
	text: string;
	iconType: IconTypes
}
