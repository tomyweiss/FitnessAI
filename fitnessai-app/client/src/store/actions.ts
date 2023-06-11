import { AppStateType }  from './reducer';

export type User = {
    userName: string;
    fullName: string;
    email: string;
    height: Number,
    weight: Number,
    sex: string
}

export interface Actions {
    ShowLogin: Function,
    HideLogin: Function,
    SetUser: Function,
    HideRegister: Function
}

export const LandingPageNumber = 0;
export const TeamPageNumber = 1;
export const AboutPageNumber = 2;
export const UserDataNumber = 3;
export const ResultsDashboardPage = 4;

export function ShowLogin(){
    return { type: AppStateType.SHOW_LOGIN }
}

export function HideLogin(){
    return { type: AppStateType.HIDE_LOGIN }
}

export function HideRegister(){
    return { type: AppStateType.HIDE_REGISTER }
}

export function SeShowRegister(){
    return { type: AppStateType.SHOW_REGISTER }
}

export function SetUserContext(user: User){
    return { type: AppStateType.SET_USER,value: user }
}

export function PageState(status:Number){
    return { type: AppStateType.SET_PAGE_STATUS, value: status }
}

export function LogOut(){
    return { type: AppStateType.LOG_OUT }
}

export function SetCounter(counter:number){
    return { type: AppStateType.SET_COUNTER, value: counter }
}

export function GetCounter(){
    return { type: AppStateType.SET_COUNTER }
}

export function SetTrainingID(trackingID:number){
    return { type: AppStateType.SET_TRAINING_ID, value: trackingID }
}