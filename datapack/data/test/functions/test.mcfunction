say hi
scoreboard objectives add test dummy " Test " 
scoreboard objectives add dmg minecraft.custom:minecraft.damage_taken " Damage " 
scoreboard players add @p test 0 
scoreboard players set @p dmg 0 
execute as @p
