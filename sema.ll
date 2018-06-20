; ModuleID = "sema.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"z" = common global i64 0, align 4
@"f" = common global double              0x0, align 4
@"g" = common global double              0x0, align 4
declare void @"func"(i64 %".1", i64 %".2") 

declare i64 @"principal"() 
