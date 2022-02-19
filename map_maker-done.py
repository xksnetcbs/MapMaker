from mcdreforged.api.all import *
import time

PLUGIN_METDATA = {
    'id': 'MAP_MAKER',
    'version': '1.0.0',
    'name': 'DCP_map_maker'
}
map_config = {
    'sx': None,
    'sz': None,
    'ex': None,
    'ez': None,
    'printy': None
}
biome_list = [
    'plains','desert', 'mountains', 'forest', 'taiga', 'swamp', 'river', 'frozen_river', 'snowy_tundra', 'snowy_mountains','ocean',
    'mushroom_fields', 'mushroom_field_shore', 'beach', 'desert_hills', 'wooded_hills','taiga_hills','jungle','jungle_hills',
    'jungle_edge','stone_shore','snowy_beach','birch_forest','birch_forest_hills','dark_forest','snowy_taiga','snowy_taiga_hills',

    'giant_tree_taiga','giant_tree_taiga_hills','wooded_mountains','savanna','savanna_plateau','badlands','wooded_badlands_plateau',
    'badlands_plateau','warm_ocean','lukewarm_ocean','cold_ocean','deep_lukewarm_ocean','deep_cold_ocean','deep_frozen_ocean',
    'bamboo_jungle','bamboo_jungle_hills', 'gravelly_mountains', 'bamboo_jungle','basalt_deltas','crimson_forest','dark_forest_hills','deep_ocean',
    'deep_lukewarm_ocean','desert_lakes','eroded_badlands','flower_forest','giant_spruce_taiga','giant_spruce_taiga_hills',

    'ice_spikes','jungle_hills','modified_badlands_plateau','modified_gravelly_mountains','modified_jungle','modified_jungle_edge',
    'modified_wooded_badlands_plateau','mountain_edge','mushroom_field_shore','mushroom_fields','shattered_savanna','shattered_savanna_plateau',
    'snowy_beach','snowy_mountains','snowy_taiga','snowy_taiga_hills','snowy_taiga_mountains','snowy_tundra','stone_shore','sunflower_plains',
    'tall_birch_forest','tall_birch_hills','wooded_badlands_plateau','wooded_hills','wooded_mountains']
biome_overworld = {
    'plains': 'stone',
    'desert': 'granite',
    'mountains': 'polished_granite',
    'forest': 'diorite',
    'taiga': 'polished_diorite',
    'swamp': 'andesite',
    'river': 'polished_andesite',
    'frozen_river': 'dirt',
    'beach':'birch_planks',
    'ocean':'orange_terracotta',
    'desert_hills':'jungle_planks',
    'taiga_hills':'dark_oak_planks',
    'jungle':'warped_planks',
    'jungle_edge':'gold_ore',
    'birch_forest':'nether_gold_ore',
    'birch_forest_hills':'oak_log',
    'dark_forest':'spruce_log',
    'giant_tree_taiga':'acacia_log',
    'giant_tree_taiga_hills':'dark_oak_log',
    'savanna':'warped_stem',
    'savanna_plateau':'stripped_oak_log',
    'badlands':'stripped_oak_log',
    'badlands_plateau':'stripped_birch_log',
    'warm_ocean':'stripped_jungle_log',
    'lukewarm_ocean':'stripped_acacia_log',
    'cold_ocean':'stripped_dark_oak_log',
    'deep_cold_ocean':'stripped_warped_stem',
    'deep_frozen_ocean':'stripped_oak_wood',
    'bamboo_jungle_hills':'stripped_birch_wood',
    'gravelly_mountains':'stripped_jungle_wood',
    'bamboo_jungle':'stripped_acacia_wood',
    'basalt_deltas':'stripped_dark_oak_wood',
    'crimson_forest':'stripped_crimson_hyphae',
    'dark_forest_hills':'stripped_warped_hyphae',
    'deep_lukewarm_ocean':'oak_wood',
    'desert_lakes':'spruce_wood',
    'eroded_badlands':'birch_wood',
    'flower_forest':'jungle_wood',
    'giant_spruce_taiga':'acacia_wood',
    'giant_spruce_taiga_hills':'dark_oak_wood',
    'ice_spikes':'crimson_hyphae',
    'jungle_hills':'warped_hyphae',
    'modified_badlands_plateau':'sponge',
    'modified_gravelly_mountains':'wet_sponge',
    'modified_jungle':'glass',
    'modified_jungle_edge':'lapis_ore',
    'modified_wooded_badlands_plateau':'lapis_block',
    'mountain_edge':'sandstone',
    'mushroom_field_shore':'chiseled_sandstone',
    'mushroom_fields':'cut_sandstone',
    'shattered_savanna':'white_wool',
    'shattered_savanna_plateau':'orange_wool',
    'snowy_beach':'magenta_wool',
    'snowy_mountains':'light_blue_wool',
    'snowy_taiga':'yellow_wool',
    'snowy_taiga_hills':'lime_wool',
    'snowy_taiga_mountains':'pink_wool',
    'snowy_tundra':'gray_wool',
    'stone_shore':'light_gray_wool',
    'sunflower_plains':'cyan_wool',
    'tall_birch_forest':'purple_wool',
    'tall_birch_hills':'blue_wool',
    'wooded_badlands_plateau':'brown_wool',
    'wooded_hills':'green_wool',
    'wooded_mountains':'red_wool',
    'deep_ocean':'lime_terracotta'
}
current_step = 0
count = 0
last = None
distance = None
alt = None
is_map_running = False
server_protect_counter = 0
print_progress = 0

def get_single_biome(server, info, x, z):
    global count, biome_list, last, server_protect_counter
    count = 0
    for i in biome_list:
        if count == 2:
            count = 0
            if last != i:
                server_protect_counter += 1
                if server_protect_counter % 4 == 0:
                    server.say("冷却中...")
                    time.sleep(1)
            last = i
            server.say("Find it!: "+alt)
            #server.say(biome_list)
            biome_list.remove(alt[10:])
            biome_list.insert(0, alt[10:])
            try:
                server.execute("execute in minecraft:the_nether run setblock " + x[:-2] + ' ' + map_config['printy'] + ' ' + z[:-2] + " " + biome_overworld[alt[10:]])
            except:
                server.say("未知的群系")
            break
        while count == 1:
            pass
        if count == 0:
            bbb = server.rcon_query("execute at overworld_scan run locatebiome " + i)
            distance = bbb[bbb.find('(') + 1:bbb.find(')') - 12]
            #server.say(bbb)
            count = 0
            if distance == '0':
                # server.say("FIND!")
                count = 2
                alt = bbb[bbb.find('minecraft:'):bbb.find("is") - 1]
    return

def digital_controller(a, b):
    a = int(a)
    b = int(b)
    a = a - (a % 8)
    b = b - (b % 8)
    if (a > b):
        return str(b), str(a)
    else: return str(a), str(b)


def main_scan(server, info):
    global current_step, print_progress
    ####准备工作：挂假人（主世界，地狱）
    ###更改sx, sz, sx, sy的位置，使sx < ex, sz < ez，并且都可以被4整除
    map_config['sx'], map_config['ex'] = digital_controller(map_config['sx'], map_config['ex'])
    map_config['sz'], map_config['ez'] = digital_controller(map_config['sz'], map_config['ez'])
    server.say("更改过的map:" + str(map_config))
    server.execute("player overworld_scan spawn at " + str(map_config['sx']) + " 256 " + str(map_config['sz']))
    server.execute("player nether_gen spawn at 0 128 0")
    time.sleep(2)
    server.execute("execute in minecraft:the_nether run tp nether_gen " + str(int(map_config['sx'])/8) + " 256 " + str(int(map_config['sz'])/8))
    sx, sz, ex, ez = int(map_config['sx']), int(map_config['sz']),int(map_config['ex']),int(map_config['ez'])


    ###更新了打印进度条：
    server.execute('bossbar add print_progress "打印进度"')
    server.execute('bossbar set minecraft:print_progress visible true')
    server.execute('bossbar set minecraft:print_progress players @a')
    width = int(map_config['ex']) - int(map_config['sx'])
    height = int(map_config['ez'])- int(map_config['sz'])
    server.execute('bossbar set minecraft:print_progress max ' + str(width * height/64)[:-2])
    ####主循环
    while sx <= ex:
        while sz <= ez:
            if is_map_running:
                get_single_biome(server, info, str(sx/8), str(sz/8))
                ###传送主世界/地狱两个假人
                server.execute("tp overworld_scan " + str(sx) + " 128 " + str(sz))
                server.execute("execute in minecraft:the_nether run tp nether_gen " + str(sx/8) + " 128 " + str(sz/8))
                sz += 8
                print_progress += 1
                server.execute("bossbar set minecraft:print_progress value " + str(print_progress))
            else:
                break
        if not is_map_running:
            break
        sx += 8
        sz = int(map_config['sz'])
    current_step = 0

def on_user_info(server, info):
    global current_step, is_map_running
    if info.content == "!!map start" and current_step == 0:
        if map_config['sx'] == None:
            current_step += 1
            server.say("请输入获取群系范围以及打印地图的y坐标(5个整数，空格隔开)：")
    elif current_step == 1:
        map_config['sx'], map_config['sz'], map_config['ex'], map_config['ez'],map_config['printy']= info.content.split(' ')
        server.say("检测到您的输入："+ str(map_config))
        current_step += 1
        server.say("您是否确认您的输入？输入!!map confirm确认并开始，输入其他取消")
    elif current_step == 2 and info.content == '!!map confirm':
        server.say("开始运行！期间请不要关闭服务端！")
        current_step = 3
        is_map_running = True
        main_scan(server, info)
    elif current_step == 2:
        server.say("操作被取消！")
        map_config['sx'], map_config['sz'], map_config['ex'], map_config['ez'] = None, None, None, None
        current_step -= 2
    elif current_step == 3 and info.content == '!!map cancel':
        server.say("操作被取消")
        map_config['sx'], map_config['sz'], map_config['ex'], map_config['ez'] = None, None, None, None
        current_step -= 2
    elif info.content == '!!map stop' and current_step == 3 and is_map_running:
        server.say("操作被取消！")
        is_map_running = False
        current_step = 0
    return

def on_info(server, info):
    global distance, count, alt
    if info.content.find("The nearest") == 0 and not info.is_user:
        distance = info.content[info.content.find('(')+1:info.content.find(')')-12]
        count = 0
        if distance == '0':
            #server.say("FIND!")
            count = 2
            alt = info.content[info.content.find('minecraft:'):info.content.find("is")-1]
