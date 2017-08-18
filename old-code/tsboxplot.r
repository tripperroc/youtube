#files = c("union-resp-all-core_number.json","union-high-all-core_number.json","union-low-all-core_number.json")
all = ("") # ("all-")
files=c("union-full-", "union-all-induced-","union-all-full-")
end="core_number.json"
files = lapply(files, function (x) paste (x, paste (all, end, sep=""), sep = ""))
da <-do.call("rbind", lapply (files, FUN=function (y) data.frame(data=unlist(lapply(fromJSON(file=y, method="C"), function(x) return (x[[1]]))), which=y)))
boxplot(data ~ which, da,outline=F)
#do.call("rbind", lapply (files, FUN=function (y) data.frame(data=unlist(lapply(fromJSON(file=y, method="C"), function(x) return (x[[1]]))), which=y)))

            
        
