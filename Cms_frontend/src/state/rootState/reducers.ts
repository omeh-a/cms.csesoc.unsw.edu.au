import { combineReducers } from "@reduxjs/toolkit";
import { reducer as foldersReducer} from 'src/state/folders/index';

export const rootReducer = combineReducers({
  folders: foldersReducer
});

export type RootState = ReturnType<typeof rootReducer>