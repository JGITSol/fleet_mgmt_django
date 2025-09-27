import { createContext, useContext, useMemo, useReducer, useState, createElement } from "react"
import { applyDelta, Event, hydrateClientStorage, useEventLoop, refs } from "$/utils/state.js"

export const initialState = {"reflex___state____state": {"is_hydrated": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "cookie": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": "", "raw_headers": {}}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}}, "reflex___state____state.pages___vehicles____vehicles_state": {"editing": null, "error": "", "form": {}, "loading": true, "show_add": false, "vehicles": []}, "reflex___state____state.pages___login____login_state": {"error": "", "password": "", "username": ""}, "reflex___state____state.reflex___state____on_load_internal_state": {}, "reflex___state____state.reflex___state____update_vars_internal_state": {}, "reflex___state____state.reflex___state____frontend_event_exception_state": {}, "reflex___state____state.pages___drivers____drivers_state": {"drivers": [], "editing": null, "error": "", "form": {}, "loading": true, "show_add": false}, "reflex___state____state.pages___maintenance____maintenance_state": {"editing": null, "error": "", "form": {}, "loading": true, "maintenance": [], "show_add": false}}

export const defaultColorMode = "system"
export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {
  reflex___state____state: createContext(null),
  reflex___state____state__pages___vehicles____vehicles_state: createContext(null),
  reflex___state____state__pages___login____login_state: createContext(null),
  reflex___state____state__reflex___state____on_load_internal_state: createContext(null),
  reflex___state____state__reflex___state____update_vars_internal_state: createContext(null),
  reflex___state____state__reflex___state____frontend_event_exception_state: createContext(null),
  reflex___state____state__pages___drivers____drivers_state: createContext(null),
  reflex___state____state__pages___maintenance____maintenance_state: createContext(null),
}
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}, "session_storage": {}}

export const state_name = "reflex___state____state"

export const exception_state_name = "reflex___state____state.reflex___state____frontend_event_exception_state"

// These events are triggered on initial load and each page navigation.
export const onLoadInternalEvent = () => {
    const internal_events = [];

    // Get tracked cookie and local storage vars to send to the backend.
    const client_storage_vars = hydrateClientStorage(clientStorage);
    // But only send the vars if any are actually set in the browser.
    if (client_storage_vars && Object.keys(client_storage_vars).length !== 0) {
        internal_events.push(
            Event(
                'reflex___state____state.reflex___state____update_vars_internal_state.update_vars_internal',
                {vars: client_storage_vars},
            ),
        );
    }

    // `on_load_internal` triggers the correct on_load event(s) for the current page.
    // If the page does not define any on_load event, this will just set `is_hydrated = true`.
    internal_events.push(Event('reflex___state____state.reflex___state____on_load_internal_state.on_load_internal'));

    return internal_events;
}

// The following events are sent when the websocket connects or reconnects.
export const initialEvents = () => [
    Event('reflex___state____state.hydrate'),
    ...onLoadInternalEvent()
]

export const isDevMode = true

export const lastCompiledTimeStamp = "2025-05-21 23:05:13.395921"

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return createElement(UploadFilesContext, {value:[filesById, setFilesById]}, children);
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectErrors] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return createElement(EventLoopContext, {value:[addEvents, connectErrors]}, children);
}

export function StateProvider({ children }) {
  const [reflex___state____state, dispatch_reflex___state____state] = useReducer(applyDelta, initialState["reflex___state____state"])
  const [reflex___state____state__pages___vehicles____vehicles_state, dispatch_reflex___state____state__pages___vehicles____vehicles_state] = useReducer(applyDelta, initialState["reflex___state____state.pages___vehicles____vehicles_state"])
  const [reflex___state____state__pages___login____login_state, dispatch_reflex___state____state__pages___login____login_state] = useReducer(applyDelta, initialState["reflex___state____state.pages___login____login_state"])
  const [reflex___state____state__reflex___state____on_load_internal_state, dispatch_reflex___state____state__reflex___state____on_load_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____on_load_internal_state"])
  const [reflex___state____state__reflex___state____update_vars_internal_state, dispatch_reflex___state____state__reflex___state____update_vars_internal_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____update_vars_internal_state"])
  const [reflex___state____state__reflex___state____frontend_event_exception_state, dispatch_reflex___state____state__reflex___state____frontend_event_exception_state] = useReducer(applyDelta, initialState["reflex___state____state.reflex___state____frontend_event_exception_state"])
  const [reflex___state____state__pages___drivers____drivers_state, dispatch_reflex___state____state__pages___drivers____drivers_state] = useReducer(applyDelta, initialState["reflex___state____state.pages___drivers____drivers_state"])
  const [reflex___state____state__pages___maintenance____maintenance_state, dispatch_reflex___state____state__pages___maintenance____maintenance_state] = useReducer(applyDelta, initialState["reflex___state____state.pages___maintenance____maintenance_state"])
  const dispatchers = useMemo(() => {
    return {
      "reflex___state____state": dispatch_reflex___state____state,
      "reflex___state____state.pages___vehicles____vehicles_state": dispatch_reflex___state____state__pages___vehicles____vehicles_state,
      "reflex___state____state.pages___login____login_state": dispatch_reflex___state____state__pages___login____login_state,
      "reflex___state____state.reflex___state____on_load_internal_state": dispatch_reflex___state____state__reflex___state____on_load_internal_state,
      "reflex___state____state.reflex___state____update_vars_internal_state": dispatch_reflex___state____state__reflex___state____update_vars_internal_state,
      "reflex___state____state.reflex___state____frontend_event_exception_state": dispatch_reflex___state____state__reflex___state____frontend_event_exception_state,
      "reflex___state____state.pages___drivers____drivers_state": dispatch_reflex___state____state__pages___drivers____drivers_state,
      "reflex___state____state.pages___maintenance____maintenance_state": dispatch_reflex___state____state__pages___maintenance____maintenance_state,
    }
  }, [])

  return (
    createElement(StateContexts.reflex___state____state,{value: reflex___state____state},
    createElement(StateContexts.reflex___state____state__pages___vehicles____vehicles_state,{value: reflex___state____state__pages___vehicles____vehicles_state},
    createElement(StateContexts.reflex___state____state__pages___login____login_state,{value: reflex___state____state__pages___login____login_state},
    createElement(StateContexts.reflex___state____state__reflex___state____on_load_internal_state,{value: reflex___state____state__reflex___state____on_load_internal_state},
    createElement(StateContexts.reflex___state____state__reflex___state____update_vars_internal_state,{value: reflex___state____state__reflex___state____update_vars_internal_state},
    createElement(StateContexts.reflex___state____state__reflex___state____frontend_event_exception_state,{value: reflex___state____state__reflex___state____frontend_event_exception_state},
    createElement(StateContexts.reflex___state____state__pages___drivers____drivers_state,{value: reflex___state____state__pages___drivers____drivers_state},
    createElement(StateContexts.reflex___state____state__pages___maintenance____maintenance_state,{value: reflex___state____state__pages___maintenance____maintenance_state},
    createElement(DispatchContext.Provider, {value: dispatchers}, children),
))))))))  )
}