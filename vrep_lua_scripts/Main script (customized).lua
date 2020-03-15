

-- Initialization part (executed just once, at simulation start) ---------
if (sim_call_type==sim.syscb_init) then
	sim.openModule(sim.handle_all)
	sim.handleGraph(sim.handle_all_except_explicit,0)
end
--------------------------------------------------------------------------

-- Regular part (executed at each simulation step) -----------------------
if (sim_call_type==sim.syscb_regular) then
	-- "Actuation"-part --
	sim.resumeThreads(sim.scriptthreadresume_default)
	sim.resumeThreads(sim.scriptthreadresume_actuation_first)
	sim.launchThreadedChildScripts()
	sim.handleChildScripts(sim.syscb_actuation)
	sim.resumeThreads(sim.scriptthreadresume_actuation_last)
	sim.handleCustomizationScripts(sim.syscb_actuation)
	sim.handleModule(sim.handle_all,false)
	simHandleJoint(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
	simHandlePath(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
	sim.handleMechanism(sim.handle_all_except_explicit)
	sim.handleIkGroup(sim.handle_all_except_explicit)
	sim.handleDynamics(sim.getSimulationTimeStep())
	simHandleVarious()
	sim.handleMill(sim.handle_all_except_explicit)

	-- "Sensing"-part --
	sim.handleCollision(sim.handle_all_except_explicit)
	sim.handleDistance(sim.handle_all_except_explicit)
	sim.handleProximitySensor(sim.handle_all_except_explicit)
	sim.handleVisionSensor(sim.handle_all_except_explicit)
	sim.resumeThreads(sim.scriptthreadresume_sensing_first)
	sim.handleChildScripts(sim.syscb_sensing)
	sim.resumeThreads(sim.scriptthreadresume_sensing_last)
	sim.handleCustomizationScripts(sim.syscb_sensing)
	sim.handleModule(sim.handle_all,true)
	sim.resumeThreads(sim.scriptthreadresume_allnotyetresumed)
	sim.handleGraph(sim.handle_all_except_explicit,sim.getSimulationTime()+sim.getSimulationTimeStep())
end
--------------------------------------------------------------------------

-- Clean-up part (executed just once, before simulation ends) ------------
if (sim_call_type==sim.syscb_cleanup) then
	sim.resetMilling(sim.handle_all)
	sim.resetMill(sim.handle_all_except_explicit)
	sim.resetCollision(sim.handle_all_except_explicit)
	sim.resetDistance(sim.handle_all_except_explicit)
	sim.resetProximitySensor(sim.handle_all_except_explicit)
	sim.resetVisionSensor(sim.handle_all_except_explicit)
	sim.closeModule(sim.handle_all)
end
--------------------------------------------------------------------------
