export type FileUploadOptions = 'resetState' | 'draggingState' | 'errorState' | 'successState';

export type ServerStatus = 'InActive' | 'Ping' | 'Active';
export type IconNames = 'Ai' | 'Shield' | 'Server';
export type Colors = 'blue' | 'green' | 'orange';

export interface MetricType {
	id: string;
	icon: IconNames;
	heading: string;
	text: string;
	color: Colors;
}
