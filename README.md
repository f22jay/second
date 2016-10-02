##深入浅出-Redux

@(ios)

原文地址：http://www.w3ctech.com/topic/1561
## 深入浅出Redux中间件
原文地址：http://www.tuicool.com/articles/u6JRjyz

中间件可以增强默认的dispatch函数，我们来看一下Redux1.0.1版本的applyMiddleware源码：
```
export default function applyMiddleware(...middlewares) {            return (next)  => 
        (reducer, initialState) => {
  var store = next(reducer, initialState);
  var dispatch = store.dispatch;
  var chain = [];
  var middlewareAPI = {
    getState: store.getState,
    dispatch: (action) => dispatch(action)
  };
  chain = middlewares.map(middleware =>
    middleware(middlewareAPI));
  dispatch = compose(...chain, store.dispatch);
  return {
    ...store,
    dispatch
  };
           };
}
```
next 参数是一个被用来创建store的函数，你可以看一下 createStore.js 源码的实现细节，传入creatStore函数，最后这个函数返回一个类似 createStore 的函数，即createStoreWithMiddleware，不同的是它包含一个由中间件加工过的dispatch实现。至于怎么加工法，看中间组件的实现了。
```
import { createStore, applyMiddleware } from ‘redux’;
import loggerMiddleware from ‘logger’;
import rootReducer from ‘../reducers’;
const createStoreWithMiddleware = 
  applyMiddleware(loggerMiddleware)(createStore);
export default function configureStore(initialState) {
  return createStoreWithMiddleware(rootReducer, initialState);
}
const store = configureStore();
```

接下来的代码将 getState 和调用原始的 dispatch 函数注入给所有的中间件：
```
var middlewareAPI = {
  getState: store.getState,
  dispatch: (action) => dispatch(action)
};
chain = middlewares.map(middleware =>
        middleware(middlewareAPI));
```
然后我们根据中间件链创建一个加工过的dispatch实现：
```
dispatch = compose(...chain, store.dispatch);

```
调用链类似下面这样
```
middlewareI(middlewareJ(middlewareK(store.dispatch)))(action)
```
现在知道为啥我们要掌握复合函数和柯里化概念了吧？最后我们只需要将新的store和调整过的dispatch函数返回即可：
```
return {
     ...store,
     dispatch
};
```
###异步中间件的理解
原文地址：http://camsong.github.io/redux-in-chinese/docs/api/applyMiddleware.html
gitlab地址：https://github.com/gaearon/redux-thunk
1.1 类似redux-thunk的实现
```
下面是类似redux-thunk的实现：

export default function thunkMiddleware({ dispatch, getState }) {
      return next => 
             action => 
                   typeof action === ‘function’ ? 
                     action(dispatch, getState) : 
                     next(action);
}
```

1.2 创建 thunk action，它是函数类型

```
function fetchSecretSauce() {
  return fetch('https://www.google.com/search?q=secret+sauce')
}

//实现thunk action，默认的输入（dispatch，getState）
function makeASandwichWithSecretSauce(forPerson) {

  // 控制反转！
  // 返回一个接收 `dispatch` 的函数。
  // Thunk middleware 知道如何把异步的 thunk action 转为普通 action。

  return function (dispatch) {
    return fetchSecretSauce().then(
      sauce => dispatch(makeASandwich(forPerson, sauce)),
      error => dispatch(apologize('The Sandwich Shop', forPerson, error))
    )
  }
}
```
1.3 像普通action一样，dispatch 异步的thunk action
```
// Thunk middleware 可以让我们像 dispatch 普通 action
// 一样 dispatch 异步的 thunk action。

store.dispatch(
  makeASandwichWithSecretSauce('Me')
)
```
结合1，2，3看看thunkMiddleware是如何工作的？

中间件在创建store时，有一个中间过程，即middlewareI(middlewareJ(middlewareK(store.dispatch)))(action)，在这里，仅仅传入了一个thunkMiddleware,那么上面可以简化成thunkMiddleware(store.dispatch)(action)。

参照1.1的实现，当传入的action类型是function类型时，调用action(dispatch,getState)。
在这个例子中，即调用makeASandwichWithSecretSauce（'Me'）(store.dispatch，nil)。
那么就是说这个thunk action里面的dispatch是从外面传过来的。

在外面看来是dispatch一个function action，看起来不可思议，正因为是加强型的dispatch（加强的地方在于middlewareI(middlewareJ(middlewareK(store.dispatch)))(action)，中间组件的逻辑实现），以及和它配合的thunk action。
##一篇比较好的React-Redux教程
原文地址：https://github.com/lewis617/react-redux-tutorial

如何执行里面的例子？
1.切换到某一个项目中，例如redux-examples中的counter路径下;
2.执行npm install
3.执行npm start，显示如下内容
```
> redux-counter-example@0.0.0 start /Users/huipingdeng/RNExamples/react-redux-tutorial-master/redux-examples/counter
> node server.js

==> 🌎  Listening on port 3000. Open up http://localhost:3000/ in your browser.
webpack built 80258babc8349c548d27 in 2735ms
```
4.在浏览器中打开http://localhost:3000/就可以看到index.html中的内容了。
## 如何理解单一state树结构
原文地址：http://www.cnblogs.com/lewis617/p/5170835.html

我们写了两个reducer，postsByReddit, selectedReddit，最后把它们合并起来。所以我们的全局单一state树的第一级节点是postsByReddit, selectedReddit。

postsByReddit节点下面就是postsByReddit返回的state，也就是[action.reddit]: posts(state[action.reddit], action)。posts()就是{ isFetching: false,didInvalidate: false, items: [] }

现在明白了全局单一state树是如何构建了的吧？----通过reducer。

###componentWillReceiveProps何时调用
state发生变化时，导致绑定的props发生了变化，此时会调用componentWillReceiveProps


