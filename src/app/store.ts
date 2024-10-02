import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { api } from './services/auth';
import authReducer from '../features/auth/authSlice';

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});

setupListeners(store.dispatch);

// integrate react-router-dom loaders with rtk ajax hooks
const buildLoaders = (api, appStore) => {
  api.loaders = {};
  Object.keys(api.endpoints).forEach((endpoint) => {
    api.loaders[endpoint] = async (params) => {
      const promise = appStore.dispatch(
        api.endpoints[endpoint].initiate(params),
      );
      await promise; // wait for data to be there
      promise.unsubscribe(); // remove the subscription. The data will stay in cache for 60 seconds and the component can subscribe to it in that timeframe.
    };
  });
};

buildLoaders(api, store);

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
