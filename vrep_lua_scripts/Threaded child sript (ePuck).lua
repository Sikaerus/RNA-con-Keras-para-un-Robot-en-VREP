threadFunction=function()

end

-- Put some initialization code here:
sim.setThreadSwitchTiming(2) -- Default timing for automatic thread switching
simRemoteApi.start(20001)

-- Here we execute the regular thread code:
res,err=xpcall(threadFunction,function(err) return debug.traceback(err) end)
if not res then
	sim.addStatusbarMessage('Lua runtime error: '..err)
end

-- Put some clean-up code here:
