import { configureStore } from '@reduxjs/toolkit';
import { User } from './actions';
export interface AppState {
  loggedIn:boolean
  user: User
  showLoginModal: boolean
  showRegisterModal: boolean
  pageStatus: number
  counter: number,
  trackingID: number
}

export enum AppStateType {
    SHOW_LOGIN = 'SHOW_LOGIN',
    HIDE_LOGIN = 'HIDE_LOGIN',
    SHOW_REGISTER = 'SHOW_REGISTER',
    HIDE_REGISTER = 'HIDE_REGISTER',
    SET_USER = 'SET_USER',
    SET_LOGGED_IN = 'SET_LOGGED_IN',
    SET_PAGE_STATUS = 'SET_PAGE_STATUS',
    LOG_OUT = 'LOGGED_OUT',
    SET_COUNTER = 'SET_COUNTER',
    SET_TRAINING_ID = 'SET_TRAINING_ID'
}

type CounterAction = SHOW_LOGIN | HIDE_LOGIN | SHOW_REGISTER | HIDE_REGISTER | SET_USER | SET_LOGGED_IN | SET_PAGE_STATUS | LOG_OUT | SET_COUNTER | SET_TRAINING_ID;

export interface SHOW_LOGIN {
    type: AppStateType.SHOW_LOGIN;
    value: boolean;
}

export interface HIDE_LOGIN {
    type: AppStateType.HIDE_LOGIN;
    value: boolean;
}

export interface SHOW_REGISTER {
    type: AppStateType.SHOW_REGISTER;
    value: boolean;
}

export interface HIDE_REGISTER {
    type: AppStateType.HIDE_REGISTER;
    value: boolean;
}

export interface SET_USER {
    type: AppStateType.SET_USER;
    value: User;
}

export interface SET_LOGGED_IN {
    type: AppStateType.SET_LOGGED_IN;
    value: boolean;
}

export interface SET_PAGE_STATUS {
    type: AppStateType.SET_PAGE_STATUS;
    value: number;
}

export interface LOG_OUT {
    type: AppStateType.LOG_OUT;
}

export interface SET_COUNTER {
    type: AppStateType.SET_COUNTER;
    value: number;
}

export interface SET_TRAINING_ID {
    type: AppStateType.SET_TRAINING_ID;
    value: number;
}
  
export function CounterReducer(state: AppState = { loggedIn: false, user: {userName:"", fullName: "", email:"", height:0, weight:0, sex: ""}, showLoginModal:false,showRegisterModal:false, pageStatus: 0, counter: 17, trackingID: 0}, action: CounterAction) {
    switch (action.type) {
      case AppStateType.SHOW_LOGIN:
        return { 
            ...state,
            showLoginModal: true
        }
        case AppStateType.HIDE_LOGIN:
            return { 
                ...state,
                showLoginModal: false
            }
        case AppStateType.SHOW_REGISTER:
            return { 
                ...state,
                showRegisterModal: true
            }
        case AppStateType.HIDE_REGISTER:
            return { 
                ...state,
                showRegisterModal: false
            }
        case AppStateType.SET_LOGGED_IN:
            return { 
                ...state,
                loggedIn: action.value
            }
        case AppStateType.SET_PAGE_STATUS:
            return { 
                ...state,
                pageStatus: action.value
            }
        case AppStateType.SET_COUNTER:
            return { 
                ...state,
                counter : action.value
            }
        case AppStateType.SET_USER:
            return { 
                ...state,
                    user: action.value,
                    loggedIn: true,
                    showLoginModal: false,
                    pageStatus: 3
                }
        case AppStateType.SET_TRAINING_ID:
            return { 
                ...state,
                trackingID: action.value
            }
        case AppStateType.LOG_OUT:
            return { 
                ...state,
                    user: {userName:"", fullName: "", email:"", height:0, weight:0, sex: ""},
                    loggedIn: false,
                    showLoginModal: false,
                    pageStatus: 0
                }
      default:
        return state;
    }
  }

export const Store = configureStore({ reducer: CounterReducer })

export type RootState = ReturnType<typeof Store.getState>

export type AppDispatch = typeof Store.dispatch