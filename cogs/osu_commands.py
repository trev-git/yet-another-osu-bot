import discord
from discord.ext import commands
from ossapi import OssapiV2

osuapi = OssapiV2("client id", "client secret", "callback url")

class OsuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def osu(self, ctx, userid):
        osu_user = osuapi.user(userid)
        embed = discord.Embed(
            title=f"Stats for {osu_user.username}", 
            type="rich", 
            url=f"https://osu.ppy.sh/users/{osu_user.id}"
        )
        embed.set_thumbnail(url=f"{osu_user.avatar_url}")
        embed.add_field(
            name="Performance:",
            value=f"--- **{osu_user.statistics.pp}pp**\n"
            f"**Global Rank:** #{osu_user.statistics.global_rank} ({osu_user.country_code}: #{osu_user.statistics.country_rank})\n"
            f"**Accuracy:** {osu_user.statistics.hit_accuracy:.2f}\n"
            f"**Play Count:** {osu_user.statistics.play_count}\n"
            f"**Level:** {osu_user.statistics.level.current}\n"
        )
        embed.add_field(
            name="Ranks:",
            value=f"**SSH**: {osu_user.statistics.grade_counts.ssh}\n"
            f"**SS**: {osu_user.statistics.grade_counts.ss}\n"
            f"**SH**: {osu_user.statistics.grade_counts.sh}\n"
            f"**S**: {osu_user.statistics.grade_counts.s}\n"
            f"**A**: {osu_user.statistics.grade_counts.a}\n"
            
        )
        await ctx.send(embed=embed)

    @commands.command(name="recent", aliases=["rs", "r"])
    async def osu_recent_play(self, ctx, userid):
        osu_user = osuapi.user(userid)
        user_scores = osuapi.user_scores(osu_user.id, 'recent')[0]
        embed = discord.Embed(
            title=f"{osuapi.beatmap(beatmap_id=user_scores.beatmap.id)._beatmapset.artist} - {osuapi.beatmap(beatmap_id=user_scores.beatmap.id)._beatmapset.title_unicode} [{user_scores.beatmap.version}]",
            url=f"https://osu.ppy.sh/beatmaps/{user_scores.beatmap.id}",
            description=f"""
            {user_scores.rank.value} > +{user_scores.mods} > {(user_scores.accuracy)*100:.2f}% > {user_scores.pp:.2f}pp
            {user_scores.score} > {user_scores.max_combo}x > `[{user_scores.statistics.count_300} / {user_scores.statistics.count_100} / {user_scores.statistics.count_50} / {user_scores.statistics.count_miss}]`
            """
        )
        embed.set_author(
            name=f"{osu_user.username}: {osu_user.statistics.pp}pp #{osu_user.statistics.global_rank} (bancho)",
            url=f"https://osu.ppy.sh/users/{osu_user.id}",
            icon_url=osu_user.avatar_url
        )
        embed.set_thumbnail(
            url=user_scores.beatmapset.covers.list
        )
        embed.set_footer(
            text=f"Ranked beatmap by {user_scores.beatmapset.creator}" if user_scores.beatmap.status.value == 1 else f"Loved beatmap by {user_scores.beatmapset.creator}",
            icon_url=osuapi.user(user_scores.beatmapset.creator).avatar_url
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OsuCommands(bot))
